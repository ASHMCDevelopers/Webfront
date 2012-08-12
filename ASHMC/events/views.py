from django.views.generic import ListView

from .models import Event

import datetime
import pytz


class EventList(ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.not_ended.order_by('start_time')

    def get_context_data(self, *args, **kwargs):
        context = super(EventList, self).get_context_data(*args, **kwargs)

        context['now'] = datetime.datetime.now(pytz.utc)

        return context
