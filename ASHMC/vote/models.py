from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext as _
# Create your models here.

from ASHMC.main.models import GradYear, Utility
from ASHMC.roster.models import Dorm, DormRoom, UserRoom
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
    VOTE_TYPES = Utility.enum('POPULARITY', 'PREFERENCE', 'SELECT_X', 'INOROUT', type_name='BallotVoteType')

    TYPES = (
        (VOTE_TYPES.POPULARITY, "Popularity"),
        (VOTE_TYPES.PREFERENCE, 'Preference'),
        (VOTE_TYPES.SELECT_X, 'Select Top X'),
        (VOTE_TYPES.INOROUT, 'Yes or No'),
    )

    vote_type = models.SmallIntegerField(default=0, choices=TYPES)
    number_to_select = models.PositiveIntegerField(blank=True, null=True)

    measure = models.ForeignKey('Measure', null=True)

    display_position = models.IntegerField(default=1)

    title = models.CharField(max_length=50)
    blurb = models.TextField()

    can_write_in = models.BooleanField(default=False)
    can_abstain = models.BooleanField(default=True)
    is_secret = models.BooleanField(default=False)

    def get_winners(self):
        """does not break ties."""
        if self.vote_type == self.VOTE_TYPES.POPULARITY or self.vote_type == self.VOTE_TYPES.INOROUT:
            max_choices = max(self.candidate_set.annotate(pv_max=models.Count('popularityvote')).values_list('pv_max', flat=True))
            return self.candidate_set.annotate(models.Count('popularityvote')).filter(popularityvote__count=max_choices)
        elif self.vote_type == self.VOTE_TYPES.PREFERENCE:
            # The lower the sum of the ranks of a candidate, the better they're doing overall.
            min_choices = min(self.candidate_set.annotate(pf_sum=models.Sum('preferentialvote__amount')).values_list('pf_sum', flat=True))
            return self.candidate_set.annotate(models.Sum('preferentialvote__amount')).filter(preferentialvote__amount=min_choices)
        elif self.vote_type == self.VOTE_TYPES.SELECT_X:
            max_choices = self.candidate_set.annotate(pv_max=models.Count('popularityvote')).order_by('-pv_max').values_list('pv_max', flat=True)[0]
            return self.candidate_set.annotate(models.Count('popularityvote')).filter(popularityvote__count=max_choices)

    def __unicode__(self):
        return u"Ballot #{}: {}".format(self.id, self.title)

    class Meta:
        unique_together = (('measure', 'title'), )

    def save(self, *args, **kwargs):
        if self.vote_type == self.VOTE_TYPES.SELECT_X and self.number_to_select is None:
            raise IntegrityError("Can't have a SELECT_X vote type and no number_to_select.")

        super(Ballot, self).save(*args, **kwargs)
        if self.vote_type == self.VOTE_TYPES.INOROUT:
            # create the two candidates now.
            yes, _ = Candidate.objects.get_or_create(
                title="Yes",
                ballot=self,
            )

            no, _ = Candidate.objects.get_or_create(
                title="No",
                ballot=self,
            )


class Measure(models.Model):
    """A collection of ballots. This is probably where you'd want
    to calculate things like quorum."""

    name = models.CharField(max_length=50)
    summary = models.TextField()

    vote_start = models.DateTimeField(default=datetime.datetime.now)
    vote_end = models.DateTimeField(null=True, blank=True,
        help_text="""If you don't specify an end time, the measure will automatically
        close the midnight after quorum is reached.""",
    )

    is_open = models.BooleanField(default=True)

    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    banned_accounts = models.ManyToManyField(User, null=True, blank=True)

    quorum = IntegerRangeField(default=50,
        help_text="Integer value between 0 and 100; what percentage of student response is quorum for this ballot?",
        max_value=100,
        min_value=0,
    )

    @property
    def actual_quorum(self):
        return Vote.objects.filter(measure=self).count()  # (float(Vote.objects.filter(measure=self).count()) / self.eligible_voters.count()) * 100

    @property
    def has_reached_quorum(self):
        return self.quorum <= self.actual_quorum

    @property
    def eligible_voters(self):
        if self.restrictions is None:
            return User.objects.filter(inactive=False)
        return self.restrictions.get_grad_year_users() & self.restrictions.get_dorm_users()

    class Meta:
        verbose_name = _('Mesure')
        verbose_name_plural = _('Mesures')

    def save(self, *args, **kwargs):
        if self.vote_end is not None:
            # Ensure that the measure is open for at least 2 days.
            if self.vote_end - self.vote_start < datetime.timedelta(days=2):
                self.vote_end = self.vote_start + datetime.timedelta(days=2)
        super(Measure, self).save(*args, **kwargs)
        # Ensures there's a restrictions object to check against in views.
        try:
            self.restrictions
        except models.ObjectDoesNotExist:
            try:
                Restrictions.objects.create(restricted_to=self)
            except IntegrityError:
                # This means that someone built in restrictions at creation time.
                pass

    def __unicode__(self):
        return u"{}".format(self.name)

    def destroy_user_associations(self):
        """This method *should* destroy the links between users
        and their votes."""
        for ballot in self.ballot_set.filter(is_secret=True):
            for vote in ballot.popularityvote_set.all():
                vote.vote = None
                vote.save()
            for vote in ballot.preferentialvote_set.all():
                vote.vote = None
                vote.save()


class Restrictions(models.Model):
    gradyears = models.ManyToManyField(GradYear, null=True, blank=True,
        help_text="Only these gradyears will be able to see this measure. If none are selected, visible to all gradyears."
    )
    dorms = models.ManyToManyField(Dorm, null=True, blank=True,
        help_text="Only residents of these dorms will be able to see this measure. If none are selected, visible to all dorms."
    )

    restricted_to = models.OneToOneField(Measure)

    class Meta:
        verbose_name_plural = _('Restrictions')

    def get_grad_year_users(self):
        if self.gradyears.all().count() == 0:
            return User.objects.all()
        user_ids = self.gradyears.all().values_list('student__user__id', flat=True)
        return User.objects.filter(id__in=[x for x in user_ids if x is not None])

    def get_dorm_users(self):
        if self.dorms.count() == 0:
            return User.objects.all()
        dormrooms = DormRoom.objects.filter(dorm__in=self.dorms.all())
        user_ids = UserRoom.objects.filter(room__in=dormrooms).values_list('user__id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def __unicode__(self):
        return u"Restrictions for {}".format(self.restricted_to)


class Vote(models.Model):

    account = models.ForeignKey(User)
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

    vote = models.ForeignKey(Vote, null=True)
    ballot = models.ForeignKey(Ballot)
    candidate = models.ForeignKey("Candidate", null=True, blank=True)

    class Meta:
        verbose_name = _('PopularityVote')
        verbose_name_plural = _('PopularityVotes')

    def __unicode__(self):
        votee = self.candidate
        return "{} ({}) for {}".format(self.vote, self.ballot, votee)


class PreferentialVote(models.Model):
    vote = models.ForeignKey(Vote, null=True)
    ballot = models.ForeignKey(Ballot)
    candidate = models.ForeignKey("Candidate")
    amount = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u"{} ({}) ranked {} at {}".format(
            self.vote,
            self.ballot,
            self.candidate.cast(),
            self.amount
        )


class Candidate(models.Model):
    """An abstract candidate, be it a person or a law or funding"""

    ballot = models.ForeignKey(Ballot)

    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    is_write_in = models.BooleanField(default=False)

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
    users = models.ManyToManyField(User, null=True, blank=True, through="CandidateUser")

    def __unicode__(self):
        return u"{}".format(
            ', '.join(
                map(
                    lambda x: x.get_full_name(),
                    self.users.all()
                )
           )
        )


class CandidateUser(models.Model):
    user = models.ForeignKey(User)
    person_candidate = models.ForeignKey(PersonCandidate)

    def save(self, *args, **kwargs):
        super(CandidateUser, self).save(*args, **kwargs)

        self.person_candidate.title = str(self.person_candidate)
        self.person_candidate.save()


def set_end_on_quorum_reached(sender, **kwargs):
    """As per Article 4, section 3, paragraph C of the Bylaws, measures end
    automatically on the midnight following quorum attainment."""
    if not 'instance' in kwargs:
        return

    obj = kwargs['instance']
    measure = obj.measure

    # Unless otherwise specified, of course.
    if measure.vote_end is not None:
        return

    if measure.actual_quorum >= measure.quorum:
        # set vote_end to midnight (technically tomorrow morning, so we add one day.)
        midnight = (timezone.now() + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        # Measures have to be open for at least 48 hours.
        if midnight - measure.vote_start >= datetime.timedelta(days=2):
            measure.vote_end = midnight

        measure.save()
#post_save.connect(set_end_on_quorum_reached, sender=Vote)
