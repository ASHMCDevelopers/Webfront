from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from ASHM.main.models import Dorm


class DormRoom(models.Model):
    """A specific room in a specific Dorm"""

    dorm = models.ForeignKey(Dorm)
    number = models.CharField(max_length=30)

    students = models.ManyToManyField(User, through="StudentRoom")

    suite = models.ForeignKey('Suite', null=True)
    tran_suite = models.ForeignKey('TransientSuite', null=True)

    class Meta:
        verbose_name = _('Dorm room')
        verbose_name_plural = _('Dorm rooms')

    def __unicode__(self):
        return u"{} {}".format(self.dorm.code, self.number)


class UserRoom(models.Model):
    """Links a User to a DormRoom"""

    student = models.ForeignKey(User)
    room = models.ForeignKey(DormRoom)

    class Meta:
        verbose_name = _('StudentRoom')
        verbose_name_plural = _('StudentRooms')

    def __unicode__(self):
        return u"{} -> {}".format(self.student, self.room)


class Suite(models.Model):

    dorm = models.ForeignKey(Dorm)

    class Meta:
        verbose_name = _('Suite')
        verbose_name_plural = _('Suites')

    def __unicode__(self):
        return u"{}: {}".format(self.dorm, self.room_set.all())


class TransientSuite(models.Model):

    name = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        verbose_name = _('TransientSuite')
        verbose_name_plural = _('TransientSuites')

    def __unicode__(self):
        return u"{}".format(self.name)
