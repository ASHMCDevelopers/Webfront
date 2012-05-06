'''
Created on Mar 30, 2012

@author: Haak Saxberg
'''
from django.conf.urls import patterns, include, url

from views import LandingPage, Writeup

urlpatterns = patterns('main.views',
                       url('^$', LandingPage.as_view(), name='landing_page'),
                       url('^writeup$', Writeup.as_view(), name='writeup'),
                       ) 