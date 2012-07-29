from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from .forms import BallotForm
from .models import Measure, DormMeasure, Vote, PopularityVote

import datetime
import pytz


class MeasureListing(ListView):
    template_name = "vote/measure_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Put the next-to-expire measures up front.
        return Measure.objects.filter(
            ~Q(id__in=Vote.objects.filter(account=self.request.user).values_list('measure__id', flat=True)),
            is_open=True,
            vote_start__lte=datetime.datetime.now(pytz.utc),
        ).exclude(
            banned_accounts__id__exact=self.request.user.id,
        ).order_by('vote_end')


class MeasureDetail(DetailView):
    model = Measure

    def get_object(self):
        object = super(MeasureDetail, self).get_object()

        # make sure it's a vote-able object.
        if not object.is_open or object.vote_end < datetime.datetime.now(pytz.utc):
            raise Http404

        if Vote.objects.filter(account=self.request.user, measure=object).count() != 0:
            raise Http404

        return object

    def get_context_data(self, *args, **kwargs):
        context = super(MeasureDetail, self).get_context_data(*args, **kwargs)

        context['forms'] = [BallotForm(b, data=self.request.POST) for b in self.get_object().ballot_set.all()]

        return context


class DormMeasureList(ListView):
    model = DormMeasure

    def get_queryset(self):
        user = self.request.user
        dorm = user.get_current_dorm  # TODO: make this a real function.

        return DormMeasure.open_objects.filter(dorm=dorm)


class ProcessVote(View):

    def post(self, request, measure_id, *args, **kwargs):
        measure = get_object_or_404(Measure, pk=measure_id)

        forms = []
        for ballot in measure.ballot_set.all():
            forms.append(BallotForm(ballot, data=request.POST, prefix="{}".format(ballot.id)))

        # Make them vote again if they fucked up
        # TODO: actually display error messages. Probably bring this
        # into one view class.
        if not all(f.is_valid() for f in forms):
            return redirect('measure_detail', pk=measure.id)

        # all forms valid - safe to create the vote.
        vote = Vote.objects.create(
            measure=measure,
            account=self.request.user,
        )

        for form in forms:
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

        return redirect('measure_list')

    def get(self, request, *args, **kwargs):
        raise PermissionDenied()
