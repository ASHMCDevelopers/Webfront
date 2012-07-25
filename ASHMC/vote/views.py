from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import Measure, DormMeasure

import datetime
import pytz


class MeasureListing(ListView):
    template_name = "vote/measure_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Put the next-to-expire measures up front.
        return Measure.objects.filter(is_open=True, vote_start__lte=datetime.datetime.now(pytz.utc)).order_by('vote_end')


class MeasureDetail(DetailView):
    model = Measure

    def get_object(self):
        object = super(MeasureDetail, self).get_object()

        # make sure it's a vote-able object.
        if not object.is_open or object.vote_end < datetime.datetime.now(pytz.utc):
            raise Http404

        return object

class DormMeasureList(ListView):
    model = DormMeasure

    def get_queryset(self):
        user = self.request.user
        dorm = user.get_current_dorm  # TODO: make this a real function.

        return DormMeasure.open_objects.filter(dorm=dorm)
