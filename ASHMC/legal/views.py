from django.conf import settings
from django.http import Http404
from django.views.generic import DetailView, TemplateView, ListView

from .models import Article, OfficialForm, GDocSheet

import gdata.docs.service
import gdata.spreadsheet.service
import socket
import tempfile
import xlrd


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


class AccountsListing(TemplateView):
    template_name = "legal/gdoc_spreadsheet.html"

    def get_context_data(self, **kwargs):
        context = super(AccountsListing, self).get_context_data(**kwargs)

        gdc = gdata.docs.service.DocsService()
        gdc.email = settings.GDOC_EMAIL
        gdc.password = settings.GDOC_PASSWORD
        gdc.source = settings.GDOC_SOURCE
        try:
            gdc.ProgrammaticLogin()
        except socket.sslerror:
            context['error'] = "Could not connect to Google Docs"
            return context

        spread = gdata.spreadsheet.service.SpreadsheetsService()
        spread.email = settings.GDOC_EMAIL
        spread.password = settings.GDOC_PASSWORD
        spread.source = settings.GDOC_SOURCE
        try:
            spread.ProgrammaticLogin()
        except socket.sslerror:
            context['error'] = "Could not connect to Google Docs"
            return context

        file_path = tempfile.mktemp(suffix=".xls")

        doc = GDocSheet.objects.get(title="ASHMC Budget")

        entry = gdc.GetDocumentListEntry(settings.GDOC_URL.format(doc.key))
        docs_auth_token = gdc.GetClientLoginToken()
        gdc.SetClientLoginToken(spread.GetClientLoginToken())
        gdc.Export(entry, file_path)
        gdc.SetClientLoginToken(docs_auth_token)

        wb = xlrd.open_workbook(file_path, formatting_info=True)
        context['wb'] = wb
        offset = int(self.kwargs['offset'] or 0)
        try:
            context['sheet'] = wb.sheets()[offset]
        except IndexError:
            raise Http404

        return context
