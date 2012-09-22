from django.contrib import admin

from .models import Dorm, DormRoom, UserRoom, Suite, TransientSuite, TransientSuiteMembership


class DormAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code', 'official_dorm')

    def queryset(self, request):
        """Show all the dorms, not just the official ones"""
        qs = self.model.all_objects.get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
admin.site.register(Dorm, DormAdmin)


class DormRoomAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'dorm', 'number')
    list_filter = ('dorm',)
admin.site.register(DormRoom, DormRoomAdmin)


class UserRoomAdmin(admin.ModelAdmin):
    def dorm(obj):
        return obj.room.dorm
    list_display = ('room', dorm, 'user',)
    list_filter = ('room__dorm', 'semesters',)
admin.site.register(UserRoom, UserRoomAdmin)


class SuiteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'dorm')
    list_filter = ('dorm', )
admin.site.register(Suite, SuiteAdmin)


class TransientSuiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(TransientSuite, TransientSuiteAdmin)


class TransientSuiteMembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(TransientSuiteMembership, TransientSuiteMembershipAdmin)
