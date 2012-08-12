from django.conf import settings
from django.core.cache import cache
from django.views.generic import ListView
from django.views.generic.base import TemplateView

#if 'courses' in settings.INSTALLED_APPS:
from ASHMC.courses.models import Course
from ASHMC.roster.models import Dorm

from .forms import LandingLoginForm
from .models import TopNewsItem, ASHMCRole, ASHMCAppointment, Semester

from blogger.models import Entry

import datetime
import pytz
from urllib2 import URLError
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
            try:
                tweets = settings.TWITTER_AGENT.statuses.user_timeline()[:6]
            except URLError:
                tweets = []
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


class ASHMCList(ListView):
    model = ASHMCAppointment

    def get_queryset(self):
        this_sem = Semester.get_this_semester()
        return self.model.objects.filter(semesters__id=this_sem.id)

    def get_context_data(self, **kwargs):
        context = super(ASHMCList, self).get_context_data(**kwargs)

        this_sem = Semester.get_this_semester()

        context['form'] = LandingLoginForm()

        this_sem_appointment = ASHMCAppointment.objects.filter(semesters__id=this_sem.id)

        context['council_main'] = {}
        context['council_additional'] = {}
        context['council_appointed'] = {}
        for title in ASHMCRole.COUNCIL_MAIN:
            key = title.lower().replace('-', '_').replace(' ', '_')
            context[key] = this_sem_appointment.filter(role__title=title)
            context['council_main'][title] = context[key]

        for title in ASHMCRole.COUNCIL_ADDITIONAL:
            key = title.lower().replace('-', '_').replace(' ', '_')
            context[key] = this_sem_appointment.filter(role__title=title)
            context['council_additional'][title] = context[key]

        for title in ASHMCRole.COUNCIL_APPOINTED:
            key = title.lower().replace('-', '_').replace(' ', '_')
            context[key] = this_sem_appointment.filter(role__title=title)
            if context[key]:
                context['council_appointed'][title] = context[key]

        context['dorms'] = Dorm.objects.all().order_by('name')

        return context


class Writeup(TemplateView):
    template_name = 'writeup.html'

    def get_context_data(self, **kwargs):
        context = super(Writeup, self).get_context_data(**kwargs)
        qcourses = Course.objects.count()\
                    - Course.active_objects.count()

        context['qcourses'] = qcourses
        context['courses'] = Course.objects.count()
        return context
