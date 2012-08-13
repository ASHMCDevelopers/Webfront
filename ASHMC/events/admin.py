from django.contrib import admin

from .models import *


admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Attendance)
admin.site.register(GuestAttendance)
