from django.contrib.auth.models import User
from django.db import models, IntegrityError

from ASHMC.roster.models import Dorm, Suite
from ASHMC.main.models import Campus, Building

import datetime
import pytz


class EventsNotOverManger(models.Manager):
    def get_query_set(self):
        return super(EventsNotOverManger, self).get_query_set().filter(end_time__gt=datetime.datetime.now(pytz.utc))


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    attendees = models.ManyToManyField(User, through="Attendance")
    guests_per_user = models.IntegerField(default=0)

    location = models.ForeignKey("Location")

    objects = models.Manager()
    not_ended = EventsNotOverManger()

    @property
    def is_today(self):
        now = datetime.datetime.now(pytz.utc)
        return self.start_time - now < datetime.timedelta(days=1)

    def __unicode__(self):
        return "{}".format(self.title)


class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    guests = models.ManyToManyField("GuestAttendance")

    class Meta:
        unique_together = (('user', 'event'),)


class GuestAttendance(models.Model):
    """For non-user attendees (i.e., registering an off-campus guest)"""
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __unicode__(self):
        return u"{}".format(self.name)


class Location(models.Model):
    campus = models.ForeignKey(Campus, default=Campus.objects.get(code='HM'))
    dorm = models.ForeignKey(Dorm, null=True, blank=True)
    suite = models.ForeignKey(Suite, null=True, blank=True)
    building = models.ForeignKey(Building, null=True, blank=True)

    def __unicode__(self):
        if self.suite:
            return u"{}: {} - {}".format(
                self.campus,
                self.suite.dorm,
                self.suite,
            )

        if self.building:
            return u"{}: {}".format(
                self.campus,
                self.building.name,
            )

        return u"{}: {}".format(
            self.campus,
            self.dorm,
        )

    def save(self, *args, **kwargs):
        if self.dorm is self.building is None:
            raise IntegrityError("Either specify a dorm or a building for this location.")
        super(Location, self).save(*args, **kwargs)
