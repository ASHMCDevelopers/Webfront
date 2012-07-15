from django.contrib import comments
from django.contrib.auth.models import User
from django.contrib.comments.models import CommentFlag
from django.contrib.markup.templatetags.markup import markdown
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from taggit.managers import TaggableManager

from .util import entries_published, DRAFT, HIDDEN, PUBLISHED, UPLOAD_TO, EntryPublishedManager
from ASHMC.main.models import Dorm

import datetime
import pytz
# Create your models here.


class Category(MPTTModel):
    """Category object for Entry"""

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(help_text=_('used for publication'),
                            unique=True, max_length=255)
    description = models.TextField(_('description'), blank=True)

    parent = TreeForeignKey('self', null=True, blank=True,
                            verbose_name=_('parent category'),
                            related_name='children')

    def entries_published(self):
        """Return only the entries published"""
        return entries_published(self.entries)

    @property
    def tree_path(self):
        """Return category's tree path, by his ancestors"""
        if self.parent:
            return '%s/%s' % (self.parent.tree_path, self.slug)
        return self.slug

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Return category's URL"""
        return ('zinnia_category_detail', (self.tree_path,))

    class Meta:
        """Category's Meta"""
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        """Category MPTT's Meta"""
        order_insertion_by = ['title']


class Entry(models.Model):
    STATUS_CHOICES = ((DRAFT, _('draft')),
                      (HIDDEN, _('hidden')),
                      (PUBLISHED, _('published')))

    title = models.CharField(_('title'), max_length=255)
    catch_title = models.CharField(max_length=50, blank=True)

    image = models.ImageField(_('image'), upload_to=UPLOAD_TO,
                              blank=True, help_text=_('used for illustration'))
    content = models.TextField(_('content'))
    excerpt = models.TextField(_('excerpt'), blank=True,
                                help_text=_('optional element'))

    tags = TaggableManager()
    categories = models.ManyToManyField(Category, verbose_name=_('categories'),
                                        related_name='entries',
                                        blank=True, null=True)
    related = models.ManyToManyField('self', verbose_name=_('related entries'),
                                     blank=True, null=True)

    slug = models.SlugField(help_text=_('used for publication'),
                            unique_for_date='creation_date',
                            max_length=255)

    authors = models.ManyToManyField(User, verbose_name=_('authors'),
                                     related_name='entries',
                                     blank=True, null=False)
    primary_author = models.ForeignKey(User)

    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)

    featured = models.BooleanField(_('featured'), default=False)

    comment_enabled = models.BooleanField(_('comment enabled'), default=True)
    comments_closed_as_of = models.DateTimeField(null=True, blank=True)

    dorms_hidden_from = models.ManyToManyField(Dorm, blank=True, null=True)  # None means not hidden

    creation_date = models.DateTimeField(_('creation date'),
                                         default=timezone.now)
    last_update = models.DateTimeField(_('last update'), default=timezone.now)
    start_publication = models.DateTimeField(_('start publication'),
                                             blank=True, null=True,
                                             help_text=_('date start publish'))
    end_publication = models.DateTimeField(_('end publication'),
                                           blank=True, null=True,
                                           help_text=_('date end publish'))

    login_required = models.BooleanField(
        _('login required'), default=False,
        help_text=_('only authenticated users can view the entry'))
    password = models.CharField(
        _('password'), max_length=50, blank=True,
        help_text=_('protect the entry with a password'))

    """template = models.CharField(
        _('template'), max_length=250,
        default='entry_detail.html',
        choices=[('entry_detail.html', _('Default template'))] + \
        ENTRY_TEMPLATES,
        help_text=_('template used to display the entry'))
    """

    objects = models.Manager()
    published = EntryPublishedManager()

    @property
    def html_content(self):
        """Return the Entry.content attribute formatted in HTML"""
        return markdown(self.content)

    @property
    def previous_entry(self):
        """Return the previous entry"""
        entries = Entry.published.filter(
            creation_date__lt=self.creation_date)[:1]
        if entries:
            return entries[0]

    @property
    def next_entry(self):
        """Return the next entry"""
        entries = Entry.published.filter(
            creation_date__gt=self.creation_date).order_by('creation_date')[:1]
        if entries:
            return entries[0]

    @property
    def word_count(self):
        """Count the words of an entry"""
        return len(strip_tags(self.html_content).split())

    @property
    def is_actual(self):
        """Check if an entry is within publication period"""
        now = timezone.now()
        if self.start_publication and now < self.start_publication:
            return False

        if self.end_publication and now >= self.end_publication:
            return False
        return True

    @property
    def is_visible(self):
        """Check if an entry is visible on site"""
        return self.is_actual and self.status == PUBLISHED

    @property
    def related_published(self):
        """Return only related entries published"""
        return entries_published(self.related)

    @property
    def discussions(self):
        """Return published discussions"""
        return comments.get_model().objects.for_model(
            self).filter(is_public=True)

    @property
    def comments(self):
        """Return published comments"""
        return self.discussions.filter(Q(flags=None) | Q(
            flags__flag=CommentFlag.MODERATOR_APPROVAL))

    @property
    def comments_are_open(self):
        """Check if comments are open"""
        return (self.comment_enabled and (self.comments_closed_as_of is None or
            timezone.localtime(datetime.datetime.now(pytz.utc)) < self.comments_closed_as_of))

    @property
    def comments_were_open(self):
        """Checks if comments were ever open."""
        return (self.comments.count() > 0 or
            self.comments_are_open)

    '''
    @property
    def short_url(self):
        """Return the entry's short url"""
        return get_url_shortener()(self)
    '''

    def __unicode__(self):
        return u'%s: %s' % (self.title, self.get_status_display())

    @models.permalink
    def get_absolute_url(self):
        """Return entry's URL"""
        creation_date = timezone.localtime(self.creation_date)
        return ('blogger_entry_detail', (), {
            'year': creation_date.strftime('%Y'),
            'month': creation_date.strftime('%m'),
            'day': creation_date.strftime('%d'),
            'slug': self.slug})

    class Meta:
        """Entry's Meta"""
        ordering = ['-creation_date']
        get_latest_by = 'creation_date'
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        permissions = (('can_view_all', 'Can view all entries'),
                       ('can_change_status', 'Can change status'),
                       ('can_change_author', 'Can change author(s)'), )
