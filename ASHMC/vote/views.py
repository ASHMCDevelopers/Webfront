from django.views.generic import ListView

from utility.models import LoginRequiredMixin as LRM

from .models import Measure


class MeasureListing(ListView, LRM):
    model = Measure
