from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from ASHMC.main.models import Dorm, Semester


class DormRoom(models.Model):
    """A specific room in a specific Dorm"""

    dorm = models.ForeignKey(Dorm)
    number = models.CharField(max_length=30)

    students = models.ManyToManyField(User, through="UserRoom")

    suite = models.ForeignKey('Suite', null=True, blank=True)
    tran_suite = models.ForeignKey('TransientSuite', null=True, blank=True)

    class Meta:
        verbose_name = _('Dorm room')
        verbose_name_plural = _('Dorm rooms')

    def __unicode__(self):
        return u"{} {}".format(self.dorm.code, self.number)


class UserRoom(models.Model):
    """Links a User to a DormRoom"""

    user = models.ForeignKey(User)
    room = models.ForeignKey(DormRoom)

    semester = models.ForeignKey(Semester)

    class Meta:
        verbose_name = _('User Room')
        verbose_name_plural = _('User Rooms')

    def __unicode__(self):
        return u"{} -> {}".format(self.user, self.room)


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
        verbose_name = _('Transient Suite')
        verbose_name_plural = _('Transient Suites')

    def __unicode__(self):
        return u"{}".format(self.name)
