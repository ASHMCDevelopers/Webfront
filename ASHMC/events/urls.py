from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import EventList, EventDetail

urlpatterns = patterns('events.views',
    url('^$', EventList.as_view(), name='event_list'),
    url('^(?P<pk>\d+)$', login_required(EventDetail.as_view()), name='event_detail'),
)
