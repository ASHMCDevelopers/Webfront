from django.views.generic import ListView, DetailView

from .models import Measure, DormMeasure


class MeasureListing(ListView):
    template_name = "vote/measure_list.html"
    paginate_by = 10

    def get_queryset(self):
        # Put the next-to-expire measures up front.
        return Measure.objects.order_by('vote_end')


class MeasureDetail(DetailView):
    model = Measure


class DormMeasureList(ListView):
    model = DormMeasure

    def get_queryset(self):
        user = self.request.user
        dorm = user.get_current_dorm  # TODO: make this a real function.

        return DormMeasure.open_objects.filter(dorm=dorm)
