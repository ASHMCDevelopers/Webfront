from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import View

from .models import TransientSuite, TransientSuiteMembership
from ASHMC.main.models import Semester


class TransientSuiteMembershipChange(View):
    def get(self, *args, **kwargs):
        raise PermissionDenied()

    def post(self, *args, **kwargs):
        tsuite = TransientSuite.objects.get(pk=kwargs['pk'])

        if kwargs['action'] == "leave":
            sem = Semester.get_this_semester()
            #print sem
            tsm = TransientSuiteMembership.objects.get(
                user=self.request.user,
                tsuite=tsuite,
            )

            #print tsm

            tsm.semesters.remove(sem)

        else:
            raise PermissionDenied()

        return redirect("main_home")
