from django.conf.urls import patterns, url

from .views import DocumentDetail, OfficialFormList, GetFormByName

urlpatterns = patterns('legal.views',
    url(r'forms$', OfficialFormList.as_view(), name='legal_form_list'),
    url(r'doc/(?P<slug>.+)', DocumentDetail.as_view(), name='legal_document_detail'),
    url(r'get/(?P<name>.+)', GetFormByName.as_view(), name='get_form_by_name'),
)
