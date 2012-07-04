from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

urlpatterns = patterns(
	'',
	url(r'^', include('blogger.urls.entries')),
	)