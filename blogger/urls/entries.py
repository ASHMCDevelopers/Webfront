"""Urls for the Blogger entries"""
from django.conf.urls import url
from django.conf.urls import patterns

from ..views.entries import EntryDetail, TaggedEntryList, AuthorEntryList


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EntryDetail.as_view(),
        name='blogger_entry_detail'
    ),
    url(r'^by_tag/(?P<tag>[a-zA-Z_]*)/$', TaggedEntryList.as_view(),
        name='blogger_tag_entry_list',
    ),
    url(r'^by_author/(?P<author_id>\d*)/$', AuthorEntryList.as_view(),
        name='blogger_author_entry_list',
    )
    )
