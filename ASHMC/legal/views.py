from django.views.generic import DetailView, TemplateView, ListView

from .models import Article, OfficialForm


class DocumentDetail(DetailView):
    model = Article

    def get_queryset(self):
        """We only want root documents here."""
        return Article.objects.filter(level=0)


class WhatIsASHMC(TemplateView):
    template_name = 'legal/what_is_ashmc.html'


class OfficialFormList(ListView):
    model = OfficialForm

    def get_queryset(self):
        names = OfficialForm.objects.all().values_list('name', flat=True)

        forms = []
        for name in names:
            forms += [OfficialForm.objects.filter(name=name).order_by('last_updated')[0]]

        return OfficialForm.objects.filter(id__in=[f.id for f in forms])
