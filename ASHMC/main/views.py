from django.conf import settings
from django.core.cache import cache
from django.views.generic.base import TemplateView  # , TemplateResponseMixin

#if 'courses' in settings.INSTALLED_APPS:
from ASHMC.courses.models import Course
from .forms import LandingLoginForm
from .models import TopNewsItem

from blogger.models import Entry

import datetime
import pytz
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
            tweets = settings.TWITTER_AGENT.statuses.user_timeline()[:6]
            for tweet in tweets:
                tweet['date'] = pytz.utc.localize(datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))

            cache.set('latest_tweets', tweets, settings.TWITTER_CACHE_TIMEOUT)

            context['latest_tweets'] = tweets

        latest_entries = Entry.published.all()[:3]
        context['latest_entries'] = latest_entries

        context['top_stories'] = TopNewsItem.objects.filter(
            date_expired__gt=datetime.datetime.now(),
            date_published__lte=datetime.datetime.now(),
            should_display=True
        ).order_by('-date_published')[:7]
        return context


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
