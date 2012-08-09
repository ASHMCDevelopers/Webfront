from django.contrib import admin

from django.utils.translation import ugettext as _

from .models import *


class DormAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'code')
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
