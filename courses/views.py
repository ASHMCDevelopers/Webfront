from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.http import HttpResponse

from .forms import CourseSearch

# Create your views here.
class CourseSearcher(TemplateResponseMixin, View):
    template_name = "course_search_results.html"
    
    def get(self, request):
        try:
            form = CourseSearch(request.GET)
        except Exception, e:
            # if there's no form, this was a bad request
            return HttpResponse(status=400)
        
        return self.render_to_response({'form':form})
        
class SplashPage(TemplateView):
    template_name = 'splash.html'
    
    def get_context_data(self, **kwargs):
        context = super(SplashPage, self).get_context_data(**kwargs)
        context['form'] = CourseSearch()
        return context


