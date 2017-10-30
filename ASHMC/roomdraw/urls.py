from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import OverallRoomListing, RoomDetail

urlpatterns = patterns('roomdraw.views',
    url(r'^listing/', login_required(OverallRoomListing.as_view()), name="roomdraw_overall_list"),
    url(r'^detail/(?P<dorm>.+)/(?P<number>.+)', login_required(RoomDetail.as_view()), name="roomdraw_room_detail"),
)
