from django.contrib import admin

from django.utils.translation import ugettext as _

from .models import *


class DormRoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(DormRoom, DormRoomAdmin)


class UserRoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserRoom, UserRoomAdmin)


class SuiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Suite, SuiteAdmin)


class TransientSuiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(TransientSuite, TransientSuiteAdmin)
