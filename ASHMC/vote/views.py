from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin


from ASHMC.main.models import Semester
from ASHMC.roster.models import UserRoom
from .forms import BallotForm
from .models import Ballot, Candidate, Measure, Vote, PopularityVote, PreferentialVote

import datetime
import pytz


class MeasureListing(ListView):
    template_name = "vote/measure_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Put the next-to-expire measures up front.

        this_sem = Semester.get_this_semester()

        try:
            room = UserRoom.objects.filter(
                user=self.request.user,
                semesters__id=this_sem.id,
            )[0].room
        except IndexError:
            # If they don't have a room, they're probably not eligible to vote.
            raise PermissionDenied()

        return Measure.objects.filter(
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


class MeasureDetail(DetailView, FormMixin):
    model = Measure

    def get_object(self):
        object = super(MeasureDetail, self).get_object()
        if self.request.user in object.banned_accounts.all():
            raise PermissionDenied()

        # make sure it's a vote-able object.
        if not object.is_open or (object.vote_end is not None and object.vote_end < datetime.datetime.now(pytz.utc)):
            raise Http404

        if Vote.objects.filter(account=self.request.user, measure=object).count() != 0:
            raise Http404

        return object

    def get_context_data(self, *args, **kwargs):
        context = super(MeasureDetail, self).get_context_data(*args, **kwargs)

        if not hasattr(self, 'bad_forms'):
            self.bad_forms = {}
        context['form_errors'] = self.bad_forms

        context['forms'] = [BallotForm(b, data=self.request.POST) for b in self.get_object().ballot_set.all()]
        context['VOTE_TYPES'] = Ballot.VOTE_TYPES

        return context

    def post(self, *args, **kwargs):
        measure = self.get_object()

        forms = []
        for ballot in measure.ballot_set.all():
            forms.append(BallotForm(ballot, data=self.request.POST, prefix="{}".format(ballot.id)))

        # Make them vote again if they fucked up
        # TODO: actually display error messages. Probably bring this
        # into one view class.
        self.bad_forms = {}
        for f in forms:
            if not f.is_valid():
                print dir(f)
                self.bad_forms[f.ballot.id] = f.errors

        if self.bad_forms:
            return self.get(*args, **kwargs)

        # all forms valid - safe to create the vote.
        vote = Vote.objects.create(
            measure=measure,
            account=self.request.user,
        )

        for form in forms:
            if form.ballot.vote_type == Ballot.VOTE_TYPES.POPULARITY:
                if form.cleaned_data['choice'] is None:
                    # Valid form with None choice means write in
                    # TODO: Document this assumption
                    pv = PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        write_in_value=form.cleaned_data['write_in_value'],
                    )
                else:
                    pv = PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=form.cleaned_data['choice'],
                    )
            elif form.ballot.vote_type == Ballot.VOTE_TYPES.SELECT_X:
                if form.cleaned_data['abstains']:
                    continue

                for candidate in form.cleaned_data['choice']:
                    pv = PopularityVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=candidate,
                    )
            elif form.ballot.vote_type == Ballot.VOTE_TYPES.PREFERENCE:
                print form.cleaned_data
                for candidate_field in form.cleaned_data:
                    candidate = Candidate.objects.get(
                        title=candidate_field,
                        ballot=form.ballot,
                    )
                    prv = PreferentialVote.objects.create(
                        ballot=form.ballot,
                        vote=vote,
                        candidate=candidate,
                        amount=form.cleaned_data[candidate_field],
                    )

        return redirect('measure_list')
