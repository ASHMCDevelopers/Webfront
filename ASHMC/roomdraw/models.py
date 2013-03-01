from django.db import models
from django.contrib.auth.models import User

from ASHMC.roster.models import DormRoom
# Create your models here.

class RoomInterest(models.Model):
    room = models.ForeignKey(DormRoom)
    interested_users = models.ManyToManyField(User)

    def __unicode__(self):
        return u"{}: {}".format(self.room, self.interested_users.all())

class DrawNumber(models.Model):
    number = models.IntegerField()
    user = models.OneToOneField(User)

    def __lt__(self, other):
        if not isinstance(other, DrawNumber):
            return NotImplemented
        # senior numbers are better than junior, etc.
        if self.user.student.class_of > other.user.student.class_of:
            return True
        # smaller numbers are better than bigger ones
        return self.number > other.number

    def __unicode__(self):
        return u"{} {}: {}".format(
            self.user.student.class_of.to_classname(),
            self.number,
            self.user,
        )
