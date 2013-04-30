from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from collections import defaultdict
import datetime
import os
import pytz
# Create your models here.


class DocumentManager(models.Manager):
    def get_query_set(self):
        return super(DocumentManager, self).get_query_set().filter(level=0)


class Modification(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey("Article")

    diff_title = models.TextField(default="", blank=True)
    diff_body = models.TextField(blank=True, default="")

    time = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"{} by {} ({})".format(
            self.article,
            self.user,
            self.time.strftime("%m/%d/%Y %H:%M"),
        )


class Article(MPTTModel):
    LEVEL_TO_HEADER_MAP = defaultdict(
        str,
        {
            1: "Article",
            2: "Section",
        }
    )

    parent = TreeForeignKey("self", null=True, blank=True, related_name='children')

    time_created = models.DateTimeField(default=datetime.datetime.now)

    modified_by = models.ManyToManyField(User, through=Modification)

    number = models.IntegerField(null=True, blank=True)
    title = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    slug = models.SlugField(null=True, blank=True, max_length=150)
    body = models.TextField(
        default="",
        blank=True,
    )

    objects = models.Manager()
    documents = DocumentManager()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        unique_together = (('number', 'title', 'level', 'parent'),)

    def __unicode__(self):
        if self.parent is not None:
            if self.title != "":
                return u"{} {}: {}".format(
                    self.LEVEL_TO_HEADER_MAP[self.level],
                    self.number,
                    self.title
                )
            return u"{}: {}".format(self.number, self.body)
        else:
            return u"{}".format(self.title)

    def save(self, *args, **kwargs):
        self.time_modified = pytz.utc.localize(datetime.datetime.now())
        if not self.slug:
            self.slug = self.title.replace(' ', '-').lower()
        super(Article, self).save(*args, **kwargs)

    def get_time_last_updated(self):
        """Exploits the tree-like structure of a legal document to find the time
        each section was modified - which is distinct from the time that a section
        itself was modified."""
        if len(self.article_set.all()) == 0:
            return max(map(lambda x: x.time, self.modification_set.all()))

        else:
            return max(map(lambda x: x.get_time_last_updated(), self.article_set.all()))

    @models.permalink
    def get_absolute_url(self):

        return ('legal_document_detail', {
                'slug': self.slug,
            })


class OfficialForm(models.Model):
    last_updated = models.DateField(default=datetime.datetime.now)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    file_actual = models.FileField(upload_to="legal/forms/%Y/%m/%d")

    @property
    def dl_url(self):
        try:
            return self.file_actual.url
        except ValueError:
            return ''

    class Meta:
        unique_together = ('name', 'last_updated')

    def __unicode__(self):
        return u"{}".format(self.name)


class MinutesDocument(models.Model):
    GROUPS = {
        1: "ASHMC",
        2: "DAC",
    }

    def update_filename(instance, filename):
        path = "legal/minutes/{}".format(datetime.date.today().year)
        format = "{}.{}".format(
            instance.date.strftime("%m-%d-%Y"),
            instance.file_actual.name.split('.')[-1]
        )
        return os.path.join(path, format)

    uploaded = models.DateField(default=datetime.datetime.now)
    date = models.DateField(unique=True)
    group = models.IntegerField(choices=GROUPS.items())

    file_actual = models.FileField(upload_to=update_filename)

    @property
    def dl_url(self):
        try:
            return self.file_actual.url
        except ValueError:
            return ''

    def __unicode__(self):
        return u"Minutes for {}".format(self.date.strftime("%d/%m/%Y"))
