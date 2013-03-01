from django.views.generic import TemplateView

from ASHMC.roster.models import Dorm, DormRoom
from .models import RoomInterest
# Create your views here.


class OverallRoomListing(TemplateView):
    template_name = "roomdraw/overall_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(OverallRoomListing, self).get_context_data(*args, **kwargs)

        rooms = []
        for dorm in Dorm.objects.all().order_by('name'):
            rooms.append(list(
                DormRoom.objects.filter(dorm=dorm).order_by('number')
            ))

        context['dorms'] = rooms

        return context
