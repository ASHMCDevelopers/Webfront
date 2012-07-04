"""Urls for the Blogger entries"""
from django.conf.urls import url
from django.conf.urls import patterns

from ..views.entries import EntryDetail


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EntryDetail.as_view(),
        name='blogger_entry_detail'),
    )
