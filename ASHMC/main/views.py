from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.base import TemplateView  # , TemplateResponseMixin

#if 'courses' in settings.INSTALLED_APPS:
from ASHMC.courses.models import Course
from .forms import LandingLoginForm
from .models import TopNewsItem

from blogger.models import Entry

import twitter
import datetime
# Create your views here.


class LandingPage(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)

        login_form = LandingLoginForm()
        context['form'] = login_form

        tweets = cache.get('latest_tweets')

        if tweets:
            context['latest_tweets'] = tweets

        else:
            tweets = twitter.Api().GetUserTimeline(settings.TWITTER_USER)[:5]
            for tweet in tweets:
                tweet.date = datetime.datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")

            cache.set('latest_tweets', tweets, settings.TWITTER_TIMEOUT)

            context['latest_tweets'] = tweets

        latest_entries = Entry.published.all()[:3]
        context['latest_entries'] = latest_entries

        context['top_stories'] = TopNewsItem.objects.filter(
            date_expired__gt=datetime.datetime.now(),
            date_published__lte=datetime.datetime.now(),
        )
        return context


class Login(View):

    def post(self, request):
        login_form = LandingLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main_home')
            else:
                return redirect('main_landing_page')

        return redirect('main_landing_page')

    def get(self, request):
        logout(request)
        return redirect('main_landing_page')


class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        return context


class Writeup(TemplateView):
    template_name = 'writeup.html'

    def get_context_data(self, **kwargs):
        context = super(Writeup, self).get_context_data(**kwargs)
        #if 'courses' in settings.INSTALLED_APPS:
        qcourses = Course.objects.count()\
                    - Course.active_objects.count()
    #    else:
    #        qcourses = 0

        context['qcourses'] = qcourses
        context['courses'] = Course.objects.count()
        return context
