from django.views.generic.base import TemplateView

# Create your views here.

class LandingPage(TemplateView):
    template_name = 'landing_page.html'
    
    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        
        return context