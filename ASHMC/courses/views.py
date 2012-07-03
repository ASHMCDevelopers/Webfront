from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django import http
from django.utils import simplejson as json
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from .forms import CourseSearch
from .models import Course, Day, Section,\
                    Enrollment

import datetime

PER_PAGE = 20
ORPHANS = 10
# Create your views here.


class CourseSearcher(TemplateResponseMixin, View):
    """
    This view class is actually an AJAX response in disguise: it filters out
    :model:`courses.Course` based on a CourseSearch form's fields.

    It creates template variables ``results``, ``total``, ``sec_filt``, and ``qs``.

    ``sec_filt`` tracks additional filtering that needs to be done to :model:`courses.Section` ; i.e.,
    when searching by exclusive day or timestart/end, we only want to show the sections
    that actually fit the search---even if the course itself has other sections that do fit.

    **Template:**

    :template:`courses/course_search_results.html`
    """

    template_name = "course_search_results.html"

    def get(self, request, page=1):
        """Typical 'get' method."""
        context = {}

        form = CourseSearch(request.GET)
        #if form.errors:
        #    raise Exception("Form not completed")
        if form.is_valid():
            qs = Course.active_objects.all()
            section_filt = Q()
            # Filter according to day preferences
            days = form.cleaned_data['days']
            if len(days) > 0:
                print 'days ', days

                if form.cleaned_data['day_limit'] == 'incl':
                    q = Q(section__meeting__timeslots__day__in=days)
                    qs = qs.filter(q)
                    section_filt = section_filt & Q(meeting__timeslots__day__in=days)
                elif form.cleaned_data['day_limit'] == 'excl':
                    # exclusion is tricky with the way we've set up models.
                    i = Q(meeting__timeslots__day__in=days)
                    edays = [x for x in Day.objects.all() if x not in days]
                    print edays
                    e = Q(meeting__timeslots__day__in=edays)
                    section_filt = i & ~e
                    s = Section.safe_objects.filter(section_filt)
                    qs = qs.filter(section__in=s)
                elif form.cleaned_data['day_limit'] == 'negl':
                    q = ~Q(section__meeting__timeslots__day__in=days)
                    qs = qs.filter(q)
                    section_filt = section_filt & ~Q(meeting__timeslots__day__in=days)
            # Filter according to campus preferences
            campuses = form.cleaned_data['campus']
            #print campuses
            if len(campuses) > 0:
                print "filtering by campus: {}".format(campuses)
                qs = qs.filter(  # Q(campus__in=campuses)|\
                               Q(codecampus__in=[x.code for x in campuses]) | \
                               Q(section__meeting__campus__in=campuses))

            #Filter according to area
            if form.cleaned_data['department']:
                print "Filtering by area: {}".format(form.cleaned_data['department'])
                qs = qs.filter(areas__id=form.cleaned_data['department'].id)

            # Filter by number
            if form.cleaned_data['numberlow'] > 0:
                qs = qs.filter(number__gte=form.cleaned_data['numberlow'])

            if form.cleaned_data['numberhigh'] is not None:
                qs = qs.filter(number__lte=form.cleaned_data['numberhigh'])

            if form.cleaned_data['timestart']:
                print 'starts: ', form.cleaned_data['timestart']
                q = Q(section__meeting__timeslots__starts__gt=form.cleaned_data['timestart'])
                qs = qs.filter(q)
                section_filt = section_filt & Q(meeting__timeslots__starts__gt=form.cleaned_data['timestart'])
            if form.cleaned_data['timeend']:
                print 'ends: ', form.cleaned_data['timeend']
                q = Q(section__meeting__timeslots__ends__lt=form.cleaned_data['timeend'])
                qs = qs.filter(q)
                section_filt = section_filt & Q(meeting__timeslots__starts__gt=form.cleaned_data['timeend'])

            #Filter according to professor
            if form.cleaned_data['professors']:
                print 'professor'
                qs = qs.filter(section__meeting__teachers=form.cleaned_data['professors'])

            if form.cleaned_data['only_open']:
                #print "only open"
                qs = qs.filter(section__is_still_open=True, section__openseats__gte=1)

            if form.cleaned_data['pf_able']:
                #print 'pf able'
                qs = qs.filter(can_passfail=True)

            if form.cleaned_data['writ_intense_only']:
                qs = qs.filter(section__is_mudd_writingintense=True)

            if form.cleaned_data['title']:
                qs = qs.filter(Q(title__icontains=form.cleaned_data['title']) |\
                               Q(description__icontains=form.cleaned_data['title']))
            if form.cleaned_data['code']:
                qs = qs.filter(Q(code__icontains=form.cleaned_data['code']))

            if form.cleaned_data['not_taken']:
                qs = qs.filter(~Q(section__enrollment__student___linked_id=request.user.id))

            if form.cleaned_data['in_reach']:
                course_ids = Enrollment.objects.filter(student=request.user.student_profile)\
                                               .values_list('section__course', flat=True)
                noreqs = qs.filter(Q(prerequisites=None))  # no prereqs

                possibles = qs.filter(Q(prerequisites__id__in=course_ids))
                # we'll take a performance hit here, but the number of courses
                # that are in possibles is likely < 200, so it's not so bad.
                for c in possibles:
                    for cid in c.prerequisites.all().values_list('id', flat=True):
                        if cid not in course_ids:
                            possibles = possibles.exclude(id=cid)
                            continue
                    for cid in c.concurrent_with.all().values_list('id', flat=True):
                        if cid not in course_ids:
                            possibles = possibles.exclude(id=cid)
                            continue
                qs = noreqs | possibles

            context['sec_filt'] = section_filt
            context['total'] = qs.count()
            context['qs'] = qs.order_by('codeletters', 'number')

            p = Paginator(context['qs'], per_page=PER_PAGE, orphans=ORPHANS, allow_empty_first_page=True)

            try:
                results = p.page(page)
            except (EmptyPage, InvalidPage):
                results = p.page(p.num_pages)

            context['results'] = results
            context['path'] = request.GET.copy().urlencode()
        else:
            context['form'] = form
        return self.render_to_response(context)


def get_nearest_day(daycode):
    DAY_MAP = {'M': 0,
               'T': 1,
               'W': 2,
               'R': 3,
               'F': 4,
               'S': 5,
               'U': 6}

    today = datetime.date.today()
    nearest = today - datetime.timedelta(today.weekday() - DAY_MAP[daycode])
    if today.weekday() is 6:
        nearest += datetime.timedelta(7)  # handles sunday oddness
    return nearest


class JSONifySectionData(View):

    def get(self, request):
        try:
            section = Section.objects.get(pk=int(request.GET['id']))
        except (KeyError, ObjectDoesNotExist):
            raise http.HttpResponseBadRequest()

        events = []
        for m in section.meeting_set.all():
            for t in m.timeslots.all():
                obj = {}
                obj['id'] = section.id
                obj['title'] = section.course.code
                obj['start'] = datetime.datetime.combine(
                                                  get_nearest_day(t.day.code),
                                                  t.starts
                                                          ).isoformat()
                obj['end'] = datetime.datetime.combine(
                                                  get_nearest_day(t.day.code),
                                                  t.ends
                                                          ).isoformat()
                obj['className'] = ['colored', m.campus.code]
                events += [obj]

        content = json.dumps(events)

        return self.get_json_response(content)

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)


class CourseDetail(TemplateResponseMixin, View):
    template_name = "course_detail.html"

    def get(self, request, cid="Q"):
        try:
            cid = int(id)
        except ValueError:
            raise http.Http404

        print cid


class SplashPage(TemplateView):
    template_name = 'splash.html'

    def get_context_data(self, **kwargs):
        context = super(SplashPage, self).get_context_data(**kwargs)
        context['form'] = CourseSearch()

        return context
