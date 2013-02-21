from django.views.generic import View, DetailView, ListView
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect

from .models import Article, OfficialForm, MinutesDocument


class DocumentDetail(DetailView):
    model = Article

    def get_queryset(self):
        """We only want root documents here."""
        return Article.objects.filter(level=0)


class OfficialFormList(ListView):
    model = OfficialForm

    def get_queryset(self):
        names = OfficialForm.objects.all().values_list('name', flat=True)

        forms = []
        for name in names:
            forms += [OfficialForm.objects.filter(name=name).order_by('last_updated')[0]]

        return OfficialForm.objects.filter(id__in=[f.id for f in forms])


class GetFormByName(View):
    def get(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name is None:
            raise Http404
        name = name.replace('_', ' ')

        # Since a form could have been updated, order by decreasing date (i.e.,
        # the most recent version will be at index 0)
        possible_forms = OfficialForm.objects.filter(name=name).order_by('last_updated')
        if possible_forms.count() < 1:
            raise Http404

        form = possible_forms[0]
        # redirect them to download the actual file.
        return redirect(form.file_actual.url)


class MinutesList(ListView):
    model = MinutesDocument

    def get_queryset(self):
        try:
            group = int(self.kwargs.get('group'))
            year = int(self.kwargs.get('year'))
        except ValueError:
            return HttpResponseBadRequest

        results = self.model.objects.filter(date__year=year, group=group)
        if not results:
            raise Http404

        return results
