'''
Created on Apr 5, 2012

@author: Haak Saxberg
'''
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('courses.views',
                       url('^$', SplashPage.as_view(), name='landing_page'),
                       url('^/find', CourseSearcher.as_view(), name='search_courses'),
                       ) 