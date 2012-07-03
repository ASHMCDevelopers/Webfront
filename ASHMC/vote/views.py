from django.views.generic import ListView

from utility.models import LoginRequiredMixin as LRM

from .models import Ballot


class BallotListing(ListView, LRM):
    model = Ballot
