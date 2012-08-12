from django.contrib.auth.models import User
from django.db import models, IntegrityError

from ASHMC.roster.models import Dorm, Suite
from ASHMC.main.models import Campus, Building


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    attendees = models.ManyToManyField(User, through="Attendance")
    guests_per_user = models.IntegerField(null=True, blank=True)

    location = models.ForeignKey("Location")

    def __unicode__(self):
        return "{}".format(self.title)


class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    guests = models.ManyToManyField("GuestAttendance")


class GuestAttendance(models.Model):
    """For non-user attendees (i.e., registering an off-campus guest)"""
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Location(models.Model):
    campus = models.ForeignKey(Campus, default=Campus.objects.get(code='HM'))
    dorm = models.ForeignKey(Dorm, null=True, blank=True)
    suite = models.ForeignKey(Suite, null=True, blank=True)
    building = models.ForeignKey(Building, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.dorm is self.building is None:
            raise IntegrityError("Either specify a dorm or a building for this location.")
        super(Location, self).save(*args, **kwargs)
