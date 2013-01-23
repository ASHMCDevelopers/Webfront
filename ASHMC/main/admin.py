from django import forms
from django.contrib import admin

from django.utils.translation import ugettext as _

from .models import *


class ASHMCRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(ASHMCRole, ASHMCRoleAdmin)


class ASHMCAppointmentAdmin(admin.ModelAdmin):
    list_filter = ('semesters',)
admin.site.register(ASHMCAppointment, ASHMCAppointmentAdmin)


class DormAppointmentAdmin(admin.ModelAdmin):
    list_filter = ('dorm_role__dorm',)
admin.site.register(DormAppointment, DormAppointmentAdmin)


class DormPrezAdmin(admin.ModelAdmin):
    pass
admin.site.register(DormPresident, DormPrezAdmin)


class DormRoleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'dorm')
    list_filter = ('dorm', 'title',)
admin.site.register(DormRole, DormRoleAdmin)


class TopNewsItemAdmin(admin.ModelAdmin):
    actions = ['set_to_display', 'set_to_undisplay']
    actions_on_top = True
    actions_on_bottom = True

    def set_to_display(self, request, queryset):
        for entry in queryset:
            entry.should_display = True
            entry.save()

        self.message_user(
            request, _('The selected items are now displayable.'))
    set_to_display.short_description = _('Mark the items as "should show"')

    def set_to_undisplay(self, request, queryset):
        for entry in queryset:
            entry.should_display = False
            entry.save()

        self.message_user(
            request, _('The selected items are no longer displayable.'))
    set_to_undisplay.short_description = _('Mark the items as "shouldn\'t show"')

admin.site.register(TopNewsItem, TopNewsItemAdmin)


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        widgets = {
          'temp_pass': forms.widgets.PasswordInput(),
        }


class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    search_fields=('user__first_name', 'user__last_name', 'middle_name', 'studentid')

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    list_display = ('studentid', first_name, last_name, 'at', 'class_of', email)
    list_filter = ('at', 'class_of')
admin.site.register(Student, StudentAdmin)


class CampusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Campus, CampusAdmin)


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('code', '__unicode__', 'campus')
    list_filter = ('campus',)
admin.site.register(Building, BuildingAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'building', )
    list_filter = ('building__campus', 'building', )
admin.site.register(Room, RoomAdmin)
