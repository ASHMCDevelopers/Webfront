from django.conf.urls import patterns, url

from .views import MeasureListing


urlpatterns = patterns('vote.views',
       url('^$', MeasureListing.as_view(), name='main_landing_page'),
       url('^measures$', MeasureListing.as_view(), name='writeup'),
)
