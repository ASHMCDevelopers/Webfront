from django.conf.urls import patterns, url

from .views import DocumentDetail

urlpatterns = patterns('legal.views',
    url(r'(?P<pk>\d+)', DocumentDetail.as_view(), name='legal_document_detail'),
)
