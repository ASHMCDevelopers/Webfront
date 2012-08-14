from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DocumentDetail, WhatIsASHMC, OfficialFormList, AccountsListing

urlpatterns = patterns('legal.views',
    url(r'about$', WhatIsASHMC.as_view(), name='about_ashmc'),
    url(r'forms$', OfficialFormList.as_view(), name='legal_form_list'),
    url(r'finances/(?P<offset>\d+)?$', login_required(AccountsListing.as_view()), name='legal_finances'),
    url(r'doc/(?P<slug>.+)', DocumentDetail.as_view(), name='legal_document_detail'),
)
