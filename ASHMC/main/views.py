from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.base import TemplateView

#if 'courses' in settings.INSTALLED_APPS:
from ASHMC.courses.models import Course
from ASHMC.roster.models import Dorm

from .forms import LandingLoginForm
from .models import TopNewsItem, ASHMCRole, ASHMCAppointment, Semester
from ASHMC.roster.models import UserRoom

from blogger.models import Entry

import datetime
import pytz
from urllib2 import URLError
# Create your views here.


class LandingPage(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)

        tweets = cache.get('latest_tweets')
        semester = Semester.get_this_semester()
        if tweets:
            context['latest_tweets'] = tweets

        else:
            try:
                tweets = settings.TWITTER_AGENT.statuses.user_timeline()[:6]
            except:
                tweets = []
            for tweet in tweets:
                tweet['date'] = pytz.utc.localize(datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))

            cache.set('latest_tweets', tweets, settings.TWITTER_CACHE_TIMEOUT)

            context['latest_tweets'] = tweets

        if self.request.user.is_authenticated():
            if self.request.user.is_superuser:
                latest_entries = Entry.published.all()
            else:
                user_dorm = UserRoom.get_current_room(self.request.user)
                try:
                    # if they're off campus, make sure the right official dorm is used:
                    if not user_dorm.room.dorm.official_dorm:
                        user_dorm = UserRoom.objects.get(
                            user=self.request.user,
                            semesters__id=semester.id,
                            room__dorm__code="OFF",
                            room__number="Symbolic Room",
                        )
                except AttributeError:
                    user_dorm = None

                except UserRoom.DoesNotExist:
                    # No offcampus room, then they're probably abroad.
                    try:
                        user_dorm = UserRoom.objects.get(
                            user=self.request.user,
                            room__dorm__code="ABR",
                            semesters__id=semester.id,
                        )

                    except UserRoom.DoesNotExist:
                        user_dorm = None

                if user_dorm:
                    latest_entries = Entry.published.exclude(
                        dorms_hidden_from__id=user_dorm.room.dorm.id,
                    )[:3]
                else:
                    latest_entries = Entry.published.filter(
                        dorms_hidden_from=None,
                    )

        else:
            latest_entries = Entry.published.filter(
                dorms_hidden_from=None,
            )

        paginator = Paginator(latest_entries, 7)
        page = self.request.GET.get('page', None)
        try:
            latest_entries = paginator.page(page)
        except PageNotAnInteger:
            latest_entries = paginator.page(1)
        except EmptyPage:
            # page out of range
            latest_entries = paginator.page(paginator.num_pages)

        context['latest_entries'] = latest_entries
        context['page'] = page

        context['top_stories'] = TopNewsItem.objects.filter(
            date_expired__gt=datetime.datetime.now(pytz.utc),
            date_published__lte=datetime.datetime.now(pytz.utc),
            should_display=True
        ).order_by('-date_published')[:7]

        #print context['top_stories']
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
