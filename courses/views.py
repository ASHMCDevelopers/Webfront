from django.views.generic.base import TemplateView

# Create your views here.

class SplashPage(TemplateView):
    template_name = 'splash.html'
    
    def get_context_data(self, **kwargs):
        context = super(SplashPage, self).get_context_data(**kwargs)
        
        return context