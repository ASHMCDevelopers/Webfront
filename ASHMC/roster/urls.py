from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import TransientSuiteMembershipChange

urlpatterns = patterns('roster.views',
                       url('^tsuite/(?P<pk>\d+)/(?P<action>.+)/', login_required(TransientSuiteMembershipChange.as_view()), name="roster_tsuite_update"),
                       )
