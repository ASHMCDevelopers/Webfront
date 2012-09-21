from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from ASHMC.main.models import ASHMCAppointment, DormPresident, Semester


class CheckHasRolePerm(ModelBackend):

    def _has_roles(self, user, titles):
        sem = Semester.get_this_semester()
        return ASHMCAppointment.objects.filter(
            reduce(lambda x, y: x | y, [Q(role__title=t) for t in titles]),
            user=user,
            semesters__id=sem.id,
        ).count() > 0

    def has_perm(self, user, perm, obj=None, **kwargs):
        print "Checking roles..."
        if user.is_superuser:
            return True
        (app_label, codename) = perm.split('.')

        if app_label == "blogger":

            if self._has_roles(user, ["President"]):
                return True

        elif app_label == 'roster':
            return False

        elif app_label == 'vote':
            if self._has_roles(user, ["President", "Vice-President"]):
                return True
            if isinstance(user.highest_ashmc_role.cast(), DormPresident):
                return True

        return super(CheckHasRolePerm, self).has_perm(user, perm, obj, **kwargs)
