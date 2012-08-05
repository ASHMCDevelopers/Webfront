'''
Created on Mar 30, 2012

@author: Haak Saxberg
'''
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from views import LandingPage, Writeup, HomePage, ASHMCList

urlpatterns = patterns('main.views',
                       url('^$', LandingPage.as_view(), name='main_landing_page'),
                       url('^writeup$', Writeup.as_view(), name='writeup'),
                       url('^home', login_required(HomePage.as_view()), name='main_home'),
                       url('^council', ASHMCList.as_view(), name="council_list"),
                       )
