from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.http import HttpResponse, Http404
from django.db.models import Count, Q


from .forms import CourseSearch
from .models import Course, RoomInfo, Day, Section, Meeting

PER_PAGE = 20

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
    
    def get(self, request):
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
                    section_filt = section_filt & q 
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
                    section_filt = section_filt & q
            # Filter according to campus preferences
            campuses = form.cleaned_data['campus']
            if len(campuses) > 0:
                print "filtering by campus: {}".format(campuses)
                qs = qs.filter(campus__in=campuses)
            
            #Filter according to area
            if form.cleaned_data['department']:
                print "Filtering by area: {}".format(form.cleaned_data['department'])
                qs = qs.filter(areas__id=form.cleaned_data['department'].id)

            # Filter by number
            if form.cleaned_data['numberlow']:
                #print 'numberlow'
                if form.cleaned_data['numberhigh']:
                    print 'numberhigh'
                    qs = qs.filter(number__gte=form.cleaned_data['numberlow'],
                                   number__lt=form.cleaned_data['numberhigh'])
                else:
                    qs = qs.filter(number=form.cleaned_data['numberlow'])
            
            
            if form.cleaned_data['timestart']:
                print 'starts: ', form.cleaned_data['timestart']
                q = Q(section__meeting__timeslots__starts__gt=form.cleaned_data['timestart'])
                qs = qs.filter(q)
                section_filt = section_filt & q
            if form.cleaned_data['timeend']:
                print 'ends: ', form.cleaned_data['timeend']
                q = Q(section__meeting__timeslots__ends__lt=form.cleaned_data['timeend'])
                qs = qs.filter(q)
                section_filt = section_filt & q
            
            
            #Filter according to professor
            if form.cleaned_data['professors']:
                #print 'professor'
                qs = qs.filter(section__meeting__teachers=form.cleaned_data['professors'])
        
            
            if form.cleaned_data['only_open']:
                #print "only open"
                qs = qs.filter(section__is_still_open=True, section__openseats__gte=1)
            
            if form.cleaned_data['pf_able']:
                #print 'pf able'
                qs = qs.filter(can_passfail=True)
            
            if form.cleaned_data['writ_intense_only']:
                qs = qs.filter(section__is_mudd_writingintense=True)
            
            context['sec_filt'] = section_filt
            context['total'] = qs.count()
            context['qs'] = qs
            context['results'] = qs.order_by('codeletters', 'number')[:PER_PAGE*2]
        else: context['form'] = form
        return self.render_to_response(context)

    
    
class SplashPage(TemplateView):
    template_name = 'splash.html'
    
    def get_context_data(self, **kwargs):
        context = super(SplashPage, self).get_context_data(**kwargs)
        context['form'] = CourseSearch()
        
        #context['courses'] = Course.active_objects.filter(num_sections__gte=2)[:PER_PAGE] 
        
        
        return context


