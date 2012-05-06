from django.views.generic.base import TemplateView

from django.conf import settings

#if 'courses' in settings.INSTALLED_APPS:
from courses.models import Course

# Create your views here.

class LandingPage(TemplateView):
    template_name = 'landing_page.html'
    
    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        
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
        