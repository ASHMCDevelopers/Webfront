from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

from ASHMC.main.models import Dorm
from ASHMC.roster.models import DormRoom, UserRoom

import datetime


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Ballot(models.Model):
    """For example, a ballot for ASHMC President would have
        candidates (actually PersonCandidates).

        Multiple ballots can appear in a measure; that is,
        you can have a ballot for ASHMC President election and
        one for VP election in the same measure.
    """

    TYPES = (
        ("PL", "Popularity"),
    )

    measure = models.ForeignKey('Measure', null=True)

    display_position = models.IntegerField(default=1)

    title = models.CharField(max_length=50)
    blurb = models.TextField()

    can_write_in = models.BooleanField(default=False)
    is_secret = models.BooleanField(default=True)

    quorum = IntegerRangeField(default=50,
        help_text="Integer value between 0 and 100; what percentage of student response is quorum for this ballot?",
        max_value=100,
        min_value=0,
    )

    def __unicode__(self):
        return u"Ballot #{}: {}".format(self.id, self.title)

    class Meta:
        unique_together = (('measure', 'display_position'), ('measure', 'title'))


class Measure(models.Model):
    """A collection of ballots. This is probably where you'd want
    to calculate things like quorum."""

    name = models.CharField(max_length=50)
    summary = models.TextField(blank=True, null=True)

    vote_start = models.DateTimeField(default=datetime.datetime.now)
    vote_end = models.DateTimeField()

    is_open = models.BooleanField(default=True)

    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    banned_accounts = models.ManyToManyField(User, null=True, blank=True)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    @property
    def eligible_voters(self):
        return User.objects.all().exclude(
            id__in=(self.banned_accounts.values_list(
                'id',
                flat=True,
            )),
        )

    class Meta:
        verbose_name = _('Mesure')
        verbose_name_plural = _('Mesures')

    def __unicode__(self):
        return u"{}: Ballots {}".format(self.name, self.ballot_set.all())

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(Measure, self).save(*args, **kwargs)


class DormMeasure(Measure):
    dorm = models.ForeignKey(Dorm)
    number = models.IntegerField()

    @property
    def eligible_voters(self):
        super_eligible = super(DormMeasure, self).eligible_voters
        user_ids = DormRoom.objects.filter(dorm=self.dorm).values_list('students__id', flat=True)
        return super_eligible.filter(id__in=user_ids)

    class Meta:
        unique_together = ('dorm', 'number',)


class Vote(models.Model):

    account = models.ForeignKey(User, null=True)
    measure = models.ForeignKey(Measure)

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        # Never vote twice.
        unique_together = (('account', 'measure'),)

    def __unicode__(self):
        return u"{} in #{}-{}".format(self.account, self.measure.id, self.measure.name)


class PopularityVote(models.Model):
    """Represents the most common kind of vote: where each student
    gets a single vote."""

    vote = models.ForeignKey(Vote)
    ballot = models.ForeignKey(Ballot)
    candidate = models.ForeignKey("Candidate", null=True, blank=True)
    write_in_value = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _('PopularityVote')
        verbose_name_plural = _('PopularityVotes')

    def __unicode__(self):
        if self.candidate is not None:
            votee = self.candidate
        else:
            votee = self.write_in_value

        return "{} ({}) for {}".format(self.vote, self.ballot, votee)


class Candidate(models.Model):
    """An abstract candidate, be it a person or a law or funding"""

    ballot = models.ForeignKey(Ballot)

    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)

 # This FK is what makes the polymorphic magic work (esp. for printing)
    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    class Meta:
        unique_together = (('ballot', 'title'),)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(Candidate, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{}".format(self.title)


class PersonCandidate(Candidate):
    users = models.ManyToManyField(User, null=True, blank=True)
