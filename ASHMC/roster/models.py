from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class OfficialDormManager(models.Manager):
    def get_query_set(self):
        return super(OfficialDormManager, self).get_query_set().filter(official_dorm=True)


class Dorm(models.Model):
    DORMS = (
        ('Atwood', 'AT'),
        ('Case', 'CA'),
        ('West', 'WE'),
        ('Sontag', "SU"),
        ("South", 'SO'),
        ('East', 'EA'),
        ('Linde', 'LI'),
        ('North', 'NO'),
        ('Brighton Park', 'BPA'),
    )
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    official_dorm = models.BooleanField(default=True)

    objects = OfficialDormManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = _('Dorm')
        verbose_name_plural = _('Dorms')

    def __unicode__(self):
        return u"{}".format(self.name)


class DormRoom(models.Model):
    """A specific room in a specific Dorm"""

    dorm = models.ForeignKey(Dorm)
    number = models.CharField(max_length=30)

    students = models.ManyToManyField(User, through="UserRoom")

    suite = models.ForeignKey('Suite', null=True, blank=True)

    class Meta:
        verbose_name = _('Dorm room')
        verbose_name_plural = _('Dorm rooms')

    def __unicode__(self):
        return u"{} {}".format(self.dorm.code, self.number)


class UserRoom(models.Model):
    """Links a User to a DormRoom"""

    user = models.ForeignKey(User)
    room = models.ForeignKey(DormRoom)

    semesters = models.ManyToManyField('main.Semester')

    class Meta:
        verbose_name = _('User Room')
        verbose_name_plural = _('User Rooms')

    def __unicode__(self):
        return u"{} -> {}".format(self.user, self.room)

    @classmethod
    def get_current_room(cls, user):
        from ASHMC.main.models import Semester
        sem = Semester.get_this_semester()
        try:
            return cls.objects.get(user=user, semesters__id=sem.id)
        except models.ObjectDoesNotExist:
            return None


class Suite(models.Model):
    name = models.CharField(max_length=100)
    dorm = models.ForeignKey(Dorm)

    class Meta:
        verbose_name = _('Suite')
        verbose_name_plural = _('Suites')
        unique_together = (('name', 'dorm'),)

    def __unicode__(self):
        return u"{}: {}".format(self.dorm, self.name)


class TransientSuite(models.Model):

    name = models.CharField(max_length=100, unique=True)

    users = models.ManyToManyField(User, through="TransientSuiteMembership")

    class Meta:
        verbose_name = _('Transient Suite')
        verbose_name_plural = _('Transient Suites')

    def __unicode__(self):
        return u"{}".format(self.name)


class TransientSuiteMembership(models.Model):
    user = models.ForeignKey(User)
    tsuite = models.ForeignKey(TransientSuite)

    semesters = models.ManyToManyField('main.Semester')

    def __unicode__(self):
        return "{} in {} ({})".format(
            self.user,
            self.tsuite,
            self.semesters.all(),
        )
