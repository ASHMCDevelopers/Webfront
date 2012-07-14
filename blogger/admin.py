from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import ManyToManyRel
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext as _

from .util import PUBLISHED, HIDDEN
from .models import Entry, new_entry, entry_updated

class EntryAdmin(admin.ModelAdmin):
    """Admin for Entry model"""
    #form = EntryAdminForm
    date_hierarchy = 'creation_date'
    fieldsets = ((_('Content'), {'fields': ('title', 'catch_title', 'content',
                                            #'image',
                                            'status',
                                            'primary_author')}),
                 (_('Options'), {'fields': ('featured', 'excerpt',  # 'template',
                                            'related', 'authors',
                                            'creation_date',
                                            'start_publication',
                                            'end_publication',
                                            'dorms_hidden_from',
                                            ),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Privacy'), {'fields': ('password', 'login_required',),
                                 'classes': ('collapse', 'collapse-closed')}),
                 (_('Discussion'), {'fields': ('comment_enabled',
                                               'comments_closed_as_of')}),
                 (_('Publication'), {'fields': ('categories', 'tags',
                                                'slug')}))
    list_filter = ('categories', 'authors', 'status', 'featured',
                   'login_required', 'comment_enabled',
                   'creation_date', 'start_publication',
                   'end_publication')
    list_display = ('get_title', 'get_authors', 'get_categories',
                    'get_tags',
                    'get_comments_are_open',
                    'get_is_actual', 'get_is_visible', 'get_link',
                     'creation_date')
    #radio_fields = {'template': admin.VERTICAL}
    filter_horizontal = ('categories', 'authors', 'related')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'excerpt', 'content', 'tags')
    actions = ['make_mine', 'make_published', 'make_hidden',
               'close_comments', 'close_pingbacks',
               'ping_directories', 'make_tweet', 'put_on_top']
    actions_on_top = True
    actions_on_bottom = True

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(EntryAdmin, self).__init__(model, admin_site)

    def get_title(self, entry):
        """Return the title with word count and number of comments"""
        title = _('%(title)s (%(word_count)i words)') % \
                {'title': entry.title, 'word_count': entry.word_count}
        comments = entry.comments.count()
        if comments:
            return _('%(title)s (%(comments)i comments)') % \
                   {'title': title, 'comments': comments}
        return title
    get_title.short_description = _('title')

    def get_authors(self, entry):
        """Return the authors in HTML"""
        """try:
            authors = ['<a href="%s" target="blank">%s</a>' %
                       (reverse('zinnia_author_detail',
                                args=[author.username]),
                        author.username) for author in entry.authors.all()]
        except NoReverseMatch:"""
        authors = [author.username for author in entry.authors.all()]
        return ', '.join(authors)
    get_authors.allow_tags = True
    get_authors.short_description = _('author(s)')

    def get_categories(self, entry):
        """Return the categories linked in HTML"""
        """try:
            categories = ['<a href="%s" target="blank">%s</a>' %
                          (category.get_absolute_url(), category.title)
                          for category in entry.categories.all()]
        except NoReverseMatch:"""
        categories = [category.title for category in
                          entry.categories.all()]
        return ', '.join(categories)
    get_categories.allow_tags = True
    get_categories.short_description = _('category(s)')

    def get_tags(self, entry):
        """Return the tags linked in HTML"""
        """try:
            return ', '.join(['<a href="%s" target="blank">%s</a>' %
                              (reverse('zinnia_tag_detail',
                                       args=[tag.name]), tag.name)
                              for tag in Tag.objects.get_for_object(entry)])
        except NoReverseMatch:"""
        return entry.tags
    get_tags.allow_tags = True
    get_tags.short_description = _('tag(s)')

    def get_sites(self, entry):
        """Return the sites linked in HTML"""
        return ', '.join(
            ['<a href="http://%(domain)s" target="blank">%(name)s</a>' %
             site.__dict__ for site in entry.sites.all()])
    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')

    def get_comments_are_open(self, entry):
        """Admin wrapper for entry.comments_are_open"""
        return entry.comments_are_open
    get_comments_are_open.boolean = True
    get_comments_are_open.short_description = _('comment enabled')

    def get_is_actual(self, entry):
        """Admin wrapper for entry.is_actual"""
        return entry.is_actual
    get_is_actual.boolean = True
    get_is_actual.short_description = _('is actual')

    def get_is_visible(self, entry):
        """Admin wrapper for entry.is_visible"""
        return entry.is_visible
    get_is_visible.boolean = True
    get_is_visible.short_description = _('is visible')

    def get_link(self, entry):
        """Return a formated link to the entry"""
        return u'<a href="%s" target="blank">%s</a>' % (
            entry.get_absolute_url(), _('View'))
    get_link.allow_tags = True
    get_link.short_description = _('View on site')

    def save_model(self, request, entry, form, change):
        """Save the authors, update time, make an excerpt"""
        if entry.status == PUBLISHED and not entry.pk:
            signal = new_entry
            entry.start_publication = timezone.now()
        else:
            signal = entry_updated

        if not form.cleaned_data.get('excerpt') and entry.status == PUBLISHED:
            entry.excerpt = Truncator('...').words(
                50, strip_tags(entry.content))

        if entry.pk and not request.user.has_perm('blogger.can_change_author'):
            form.cleaned_data['authors'] = entry.authors.all()

        if not form.cleaned_data.get('authors'):
            form.cleaned_data['authors'].append(request.user)

        entry.last_update = timezone.now()
        entry.save()
        signal.send(sender=self, entry_id=entry.pk, author_id=request.user.id)

    def queryset(self, request):
        """Make special filtering by user permissions"""
        queryset = super(EntryAdmin, self).queryset(request)
        if request.user.has_perm('blogger.can_view_all'):
            return queryset
        return request.user.entries.all()

    def make_mine(self, request, queryset):
        """Set the entries to the user"""
        for entry in queryset:
            if request.user not in entry.authors.all():
                entry.authors.add(request.user)
        self.message_user(
            request, _('The selected entries now belong to you.'))
    make_mine.short_description = _('Set the entries to the user')

    def make_published(self, request, queryset):
        """Set entries selected as published"""
        queryset.update(status=PUBLISHED)
        self.ping_directories(request, queryset, messages=False)
        self.message_user(
            request, _('The selected entries are now marked as published.'))
    make_published.short_description = _('Set entries selected as published')

    def make_hidden(self, request, queryset):
        """Set entries selected as hidden"""
        queryset.update(status=HIDDEN)
        self.message_user(
            request, _('The selected entries are now marked as hidden.'))
    make_hidden.short_description = _('Set entries selected as hidden')

admin.site.register(Entry, EntryAdmin)
