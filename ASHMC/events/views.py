from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from .forms import AttendanceForm
from .models import Event, Attendance, GuestAttendance

import datetime
import pytz


class EventList(ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        # Show events that are ending sooner first
        return Event.not_ended.order_by('end_time')

    def get_context_data(self, *args, **kwargs):
        context = super(EventList, self).get_context_data(*args, **kwargs)

        context['now'] = datetime.datetime.now(pytz.utc)

        return context


class EventDetail(DetailView, FormMixin):
    model = Event
    form_class = AttendanceForm

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetail, self).get_context_data(*args, **kwargs)

        context['form'] = AttendanceForm(context['object'], self.request.POST)

        try:
            context['attendance'] = Attendance.objects.get(
                user=self.request.user,
                event=self.get_object(),
            )
        except:
            context['attendance'] = None

        return context

    def post(self, *args, **kwargs):
        event = self.get_object()
        f = AttendanceForm(event, self.request.POST)
        if not f.is_valid():
            return self.get(*args, **kwargs)

        a, _ = Attendance.objects.get_or_create(
            user=self.request.user,
            event=event,
        )

        if not _:
            # get rid of the guests, and the attendance
            a.guests.all().delete()
            a.delete()
            return self.get(*args, **kwargs)

        for number in range(1, event.guests_per_user + 1):
            try:
                name = f.cleaned_data['name_{}'.format(number)]
                age = f.cleaned_data['age_{}'.format(number)]

                if age is None:
                    continue

                g = GuestAttendance.objects.create(
                    name=name,
                    age=age,
                )
                a.guests.add(g)
            except KeyError:
                pass

        return redirect('event_list')
