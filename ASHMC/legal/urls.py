from django.conf.urls import patterns, url

from .views import DocumentDetail

urlpatterns = patterns('legal.views',
    url(r'(?P<slug>.+)', DocumentDetail.as_view(), name='legal_document_detail'),
)
