from django.db import models
from django.utils import timezone

from django.conf import settings

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2

UPLOAD_TO = settings.MEDIA_ROOT + 'blog_image_uploads/'


def entries_published(queryset):
    """Return only the entries published"""
    now = timezone.now()
    return queryset.filter(
        models.Q(start_publication__lte=now) | \
        models.Q(start_publication=None),
        models.Q(end_publication__gt=now) | \
        models.Q(end_publication=None),
        status=PUBLISHED)


class EntryPublishedManager(models.Manager):
    """Manager to retrieve published entries"""

    def get_query_set(self):
        """Return published entries"""
        return entries_published(
            super(EntryPublishedManager, self).get_query_set())

    def on_site(self):
        """Return entries published on current site"""
        return super(EntryPublishedManager, self).get_query_set(
            )

    def search(self, pattern):
        """Top level search method on entries"""
        try:
            return self.advanced_search(pattern)
        except:
            return self.basic_search(pattern)

    def advanced_search(self, pattern):
        """Advanced search on entries"""
        from zinnia.search import advanced_search
        return advanced_search(pattern)

    def basic_search(self, pattern):
        """Basic search on entries"""
        lookup = None
        for pattern in pattern.split():
            query_part = models.Q(content__icontains=pattern) | \
                         models.Q(excerpt__icontains=pattern) | \
                         models.Q(title__icontains=pattern)
            if lookup is None:
                lookup = query_part
            else:
                lookup |= query_part

        return self.get_query_set().filter(lookup)
