from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import OverallRoomListing

urlpatterns = patterns('roomdraw.views',
    url(r'^listing/', login_required(OverallRoomListing.as_view()), name="roomdraw_overall_list"),
)
