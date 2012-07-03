from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class Role(models.Model):

    year = models.IntegerField()
    title = models.CharField(max_length=50)

    student = models.ForeignKey(User)

    class Meta:
        abstract = True


class ASHMCRole(Role):
    """Describes a role in ASHMC, i.e. President"""

    def __unicode__(self):
        return u"ASHMC {}".format(self.title)

    def short_repr(self):
        return u"{}".format(self.title)


class DormPresident(ASHMCRole):
    """Subclass of ASHMCRole specifically for Dorm Presidents, since they have to be associated
    with a dorm."""

    dorm = models.ForeignKey('Dorm')

    def __unicode__(self):
        return u"{} {}".format(self.dorm, self.title)


class Dorm(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name = _('Dorm')
        verbose_name_plural = _('Dorms')

    def __unicode__(self):
        return u"{}".format(self.name)


class DormRole(Role):

    dorm = models.ForeignKey(Dorm)

    class Meta:
        verbose_name = _('DormRole')
        verbose_name_plural = _('DormRoles')

    def __unicode__(self):
        return u"{} {}".format(self.dorm, self.title)


class DormRoom(models.Model):

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


class StudentRoom(models.Model):

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

class TopNews(models.Model):

    slug = models.CharField(max_length=80)
    panel_html = models.TextField()
    panel_css = models.TextField()

    author = models.ForeignKey(User)
    date_published = models.DateTimeField()
    date_expired = models.DateTimeField()
