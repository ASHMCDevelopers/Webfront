'''
Created on Apr 5, 2012

@author: haak
'''
from django.conf.urls import patterns, include, url

from django.contrib.auth.decorators import login_required

from views import SplashPage

urlpatterns = patterns('courses.views',
                       url('^$', SplashPage.as_view(), name='landing_page'),
                       ) 