from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.


class Role(models.Model):

    year = models.IntegerField()
    title = models.CharField(max_length=50)

    student = models.ForeignKey(User)

    # This FK is what makes the polymorphic magic work (esp. for printing)
    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
        super(Role, self).save(*args, **kwargs)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    class Meta:
        abstract = True


class ASHMCRole(Role):
    """Describes a role in ASHMC, i.e. President"""
    COUNCIL_ROLES = (
        'President',
        'Vice-President',
        'Dorm President',
        'Treasurer',
        'Webmaster',
        'Student',
    )

    def __lt__(self, other):
        assert isinstance(other, ASHMCRole)
        try:
            my_index = ASHMCRole.COUNCIL_ROLES.index(self.title)
        except ValueError:
            my_index = ASHMCRole.COUNCIL_ROLES.index("Dorm President")

        try:
            their_index = ASHMCRole.COUNCIL_ROLES.index(other.title)
        except ValueError:
            their_index = ASHMCRole.COUNCIL_ROLES.index("Dorm President")

        return my_index > their_index

    def __unicode__(self):
        return u"ASHMC {}".format(self.title)

    def short_repr(self):
        return u"{}".format(self.title)

setattr(User, "highest_ashmc_role", property(lambda x: max(x.ashmcrole_set.all())))


class DormPresident(ASHMCRole):
    """Subclass of ASHMCRole specifically for Dorm Presidents, since they have to be associated
    with a dorm."""

    dorm = models.ForeignKey('Dorm')

    def __unicode__(self):
        if self.title == " ":
            return u"{} President".format(self.dorm)
        else:
            return u"{} President {}".format(self.dorm, self.title)


class Dorm(models.Model):
    DORMS = (
        ('Atwood', 'AT'),
        ('Case', 'CA'),
        ('West', 'WE'),
        ('Sontag', "SU"),
        ("South", 'SO'),
        ('EAST', 'EA'),
        ('Linde', 'LI'),
        ('North', 'NO'),
        ('Brighton Park', 'BPA'),
    )
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


class TopNewsItem(models.Model):

    slug = models.CharField(max_length=80)
    panel_html = models.TextField()
    panel_css = models.TextField()
    render_css = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User)
    date_published = models.DateTimeField()
    date_expired = models.DateTimeField()

    def __unicode__(self):
        return u"{}".format(self.slug)

    def save(self, *args, **kwargs):
        if self.id is None:
            super(TopNewsItem, self).save(*args, **kwargs)
            self.save(*args, **kwargs)

        # TODO: Make this less janky
        css = self.panel_css
        lines = []
        for line in css.split('\n'):
            lines += ["#slider{} {}".format(self.id, line)]

        self.render_css = '\n'.join(lines)

        super(TopNewsItem, self).save(*args, **kwargs)
