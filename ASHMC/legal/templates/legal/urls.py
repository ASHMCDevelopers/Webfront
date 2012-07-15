from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from views import LandingPage, Writeup, Login, HomePage

urlpatterns = patterns('main.views',
                       url('^$', LandingPage.as_view(), name='main_landing_page'),
                       url('^writeup$', Writeup.as_view(), name='writeup'),
                       url('^home', login_required(HomePage.as_view()), name='main_home'),
                       url('^login$', Login.as_view(), name="login"),
                       url('^logout$', Login.as_view(), name="logout"),
                       )
