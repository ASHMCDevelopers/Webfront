from django.views.generic import TemplateView, DetailView

from ASHMC.roster.models import Dorm, DormRoom
from .models import RoomInterest

from collections import defaultdict
# Create your views here.


class OverallRoomListing(TemplateView):
    template_name = "roomdraw/overall_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(OverallRoomListing, self).get_context_data(*args, **kwargs)

        rooms = []
        for dorm in Dorm.objects.all().exclude(name="Off Campus").order_by('name'):
            rooms.append(list(
                DormRoom.objects.filter(dorm=dorm).order_by('number')
            ))

        context['dorms'] = rooms
        floors = defaultdict(lambda: range(1,3))
        floors["Atwood"] = range(1, 4)
        floors["Brighton Park"] = []
        context['floors'] = floors

        return context

class RoomDetail(DetailView):
    model = DormRoom
    template_name = "roomdraw/dormroom_detail.html"

    def get_object(self):
        dorm_code = self.kwargs.get('dorm')
        number = self.kwargs.get('number')

        return DormRoom.objects.get(dorm__code=dorm_code, number=number)
