'''
Created on Apr 5, 2012

@author: Haak Saxberg
'''
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('courses.views',
                       url('^find$', CourseSearcher.as_view(), name='search_courses'),
                       url('^find/(?P<page>\d+)', CourseSearcher.as_view(), name='search_courses_page'),
                       url('^calendar/make_section_json$', JSONifySectionData.as_view(), name='create_calendar_data'),
                       url('^', SplashPage.as_view(), name='landing_page'),
                       ) 