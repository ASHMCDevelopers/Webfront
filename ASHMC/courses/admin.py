from django.contrib import admin

from .models import *


class PrereqAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'course', 'requisite')
admin.site.register(Prerequisite, PrereqAdmin)


class MajorCourseRequirementAdmin(admin.ModelAdmin):
    pass
admin.site.register(MajorCourseRequirement, MajorCourseRequirementAdmin)


class MajorCourseRequirementInline(admin.TabularInline):
    model = MajorCourseRequirement
    extra = 1


class MajorAdmin(admin.ModelAdmin):
    def studentcount(self):
        return self.students.count()
    list_display = ('title', studentcount, 'primary_campus')
    list_filter = ('primary_campus', 'departments__campus', 'departments',)
    inlines = (MajorCourseRequirementInline,)
admin.site.register(Major, MajorAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'campus', 'number')
    list_filter = ('needs_attention', 'campus', 'departments', 'areas', )

admin.site.register(Course, CourseAdmin)


class CourseAreaAdmin(admin.ModelAdmin):
    list_filter = ('is_req_area', 'hard_science')
admin.site.register(CourseArea, CourseAreaAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_filter = ('needs_attention', )
admin.site.register(Section, SectionAdmin)


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'day', 'starts', 'ends')
    list_filter = ('day', 'starts', 'ends')
admin.site.register(Timeslot, TimeslotAdmin)


class RoomInfoInline(admin.TabularInline):
    model = RoomInfo
    extra = 1


class RoomInfoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'room', 'timeslot',)
    list_filter = ('is_tba', 'is_arr')
admin.site.register(RoomInfo, RoomInfoAdmin)


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('get_timeslot_tuples', 'section', 'meeting_code')
    list_filter = ('needs_attention',)
    inlines = (RoomInfoInline,)
admin.site.register(Meeting, MeetingAdmin)


class EnrollmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Enrollment, EnrollmentAdmin)


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',)
    list_filter = ('departments__code', 'departments__campus')
admin.site.register(Professor, ProfessorAdmin)


class DeptAdmin(admin.ModelAdmin):
    list_filter = ('campus',)
admin.site.register(Department, DeptAdmin)


class DayAdmin(admin.ModelAdmin):
    pass
admin.site.register(Day, DayAdmin)


class SemesterAdmin(admin.ModelAdmin):
    list_filter = ('year', 'half')
admin.site.register(Semester, SemesterAdmin)
