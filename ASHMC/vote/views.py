from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView


from ASHMC.main.models import ASHMCRole, Semester
from ASHMC.roster.models import UserRoom
from .forms import BallotForm
from .models import Ballot, Candidate, Measure, Vote, PopularityVote, PreferentialVote

import datetime
import logging
import pytz


logger = logging.getLogger(__name__)


class CreateMeasure(CreateView):
    model = Measure


class MeasureListing(ListView):
    template_name = "vote/measure_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Put the next-to-expire measures up front.

        this_sem = Semester.get_this_semester()

        if self.request.user.is_superuser:
            return Measure.objects.exclude(vote_end__lte=datetime.datetime.now(pytz.utc)).order_by('vote_end')

        try:
            room = UserRoom.objects.filter(
                user=self.request.user,
                semesters__id=this_sem.id,
                room__dorm__official_dorm=True,
            )[0].room
        except IndexError:
            # If they don't have a room, they're probably not eligible to vote.
            #raise PermissionDenied()
            logger.info("blocked access to {}".format(self.request.user))
            # Until we have roster data importing, this is bad
            pass

        return Measure.objects.exclude(
            # Immediately filter out expired measures. Otherwise shit gets weird.
            vote_end__lte=datetime.datetime.now(pytz.utc),
        ).filter(
            # Hide measures that the user has already voted in.
            ~Q(id__in=Vote.objects.filter(account=self.request.user).values_list('measure__id', flat=True)),
            Q(restrictions__dorms=room.dorm) | Q(restrictions__dorms=None),
            Q(restrictions__gradyears=self.request.user.student.class_of) | Q(restrictions__gradyears=None),
            is_open=True,
            # Only show measures which have already opened for voting
            vote_start__lte=datetime.datetime.now(pytz.utc),
        ).exclude(
            banned_accounts__id__exact=self.request.user.id,
        ).order_by('vote_end')

    def get_context_data(self, *args, **kwargs):
        context = super(MeasureListing, self).get_context_data(*args, **kwargs)

        # Get the last measure the user voted on, and clear it.
        last_measure_voted_id = self.request.session.pop('VOTE_LAST_MEASURE_ID', None)
        if last_measure_voted_id:
            context['last_measure_voted'] = Measure.objects.get(pk=last_measure_voted_id)

        return context


class MeasureDetail(DetailView):
    model = Measure

    def get_object(self):
        object = super(MeasureDetail, self).get_object()
        if self.request.user in object.banned_accounts.all():
            raise PermissionDenied()

        # make sure it's a vote-able object.
        if not object.is_open or (object.vote_end is not None and object.vote_end < datetime.datetime.now(pytz.utc)):
            logger.info('{} attempted vote on closed measure {}'.format(self.request.user, object))
            raise Http404

        if self.request.user not in object.eligible_voters:
            logger.info("{} attempted to vote in disallowed measure {}".format(self.request.user, object))
            raise Http404

        if Vote.objects.filter(account=self.request.user, measure=object).count() != 0:
            raise Http404

        return object

    def get_context_data(self, *args, **kwargs):
        context = super(MeasureDetail, self).get_context_data(*args, **kwargs)

        if not hasattr(self, 'bad_forms'):
            self.bad_forms = {}
        context['form_errors'] = self.bad_forms

        context['forms'] = [BallotForm(b, data=self.request.POST) for b in self.get_object().ballot_set.all().order_by('display_position')]
        context['VOTE_TYPES'] = Ballot.VOTE_TYPES

        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return redirect('measure_list')
        measure = self.get_object()

        forms = []
        for ballot in measure.ballot_set.all():
            forms.append(BallotForm(ballot, data=self.request.POST, prefix="{}".format(ballot.id)))

        # Make them vote again if they fucked up
        self.bad_forms = {}
        for f in forms:
            if not f.is_valid():
                self.bad_forms[f.ballot.id] = f.errors

        if self.bad_forms:
            logger.info("bad forms on {} from {}".format(
                    [f.ballot.id for f in forms],
                    self.request.user
                )
            )
            return self.get(*args, **kwargs)

        # all forms valid - safe to create the vote.
        vote = Vote.objects.create(
            measure=measure,
            account=self.request.user,
        )

        for form in forms:
            if form.ballot.vote_type == Ballot.VOTE_TYPES.POPULARITY:
                if form.cleaned_data['choice'] is None:
                    # Valid form with None choice means write in or abstain
                    if not (form.cleaned_data['write_in_value'] or '').strip():
                        # An "empty" (e.g., whitespace-only) write-in is caught
                        # during form validation, so if we get here that means
                        # they're really abstaining.
                        continue

                    c, _ = Candidate.objects.get_or_create(
                        title=form.cleaned_data['write_in_value'],
                        ballot=form.ballot,
                        is_write_in=True,
                    )
                    PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=c,
                    )
                else:
                    PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=form.cleaned_data['choice'],
                    )

            elif form.ballot.vote_type == Ballot.VOTE_TYPES.SELECT_X:
                for candidate in form.cleaned_data['choice']:
                    PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=candidate,
                    )

            elif form.ballot.vote_type == Ballot.VOTE_TYPES.PREFERENCE:
                for candidate_field in form.cleaned_data:
                    candidate = Candidate.objects.get(
                        title=candidate_field,
                        ballot=form.ballot,
                    )
                    PreferentialVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=candidate,
                        amount=form.cleaned_data[candidate_field],
                    )

            elif form.ballot.vote_type == Ballot.VOTE_TYPES.INOROUT:
                # Don't create a popularityvote if their choice is 'abstain'
                if form.cleaned_data['choice']:
                    PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=form.cleaned_data['choice']
                    )

        # Store the voted-on measure for confirmation
        self.request.session['VOTE_LAST_MEASURE_ID'] = measure.id
        logger.info('new vote {} from {}'.format(vote.id, self.request.user))
        return redirect('measure_list')


class MeasureResultList(ListView):
    model = Measure
    template_name = 'vote/measure_results.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Measure.objects.all().order_by('-vote_end')

        this_sem = Semester.get_this_semester()
        try:
            room = UserRoom.objects.filter(
                user=self.request.user,
                semesters__id=this_sem.id,
                room__dorm__official_dorm=True,
            )[0].room
        except IndexError:
            # If they don't have a room, they're probably not eligible to vote.
            raise PermissionDenied()

        if self.request.user.highest_ashmc_role >= ASHMCRole.objects.get(title="Vice-President"):
            # VP's and higher can see all measures, except those that are dorm-specific
            # because ASHMC has no business within a dorm.
            return Measure.objects.filter(
                Q(restrictions__dorms=room.dorm) | Q(restrictions__dorms=None),
                Q(vote_end__lte=datetime.datetime.now(pytz.utc)) | Q(is_open=False),
            ).order_by('-vote_end')

        return Measure.objects.filter(
            Q(restrictions__dorms=room.dorm) | Q(restrictions__dorms=None),
            Q(restrictions__gradyears=self.request.user.student.class_of) | Q(restrictions__gradyears=None),
            # Only show measures which have already closed for voting
            vote_end__lte=datetime.datetime.now(pytz.utc),
        ).exclude(
            banned_accounts__id__exact=self.request.user.id,
        ).order_by('-vote_end')

