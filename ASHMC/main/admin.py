from django.contrib import admin

from .models import *


class ASHMCRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(ASHMCRole, ASHMCRoleAdmin)


class DormPrezAdmin(admin.ModelAdmin):
    pass
admin.site.register(DormPresident, DormPrezAdmin)


class DormAdmin(admin.ModelAdmin):
    pass
admin.site.register(Dorm, DormAdmin)


class DormRoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(DormRole, DormRoleAdmin)


class TopNewsAdmin(admin.ModelAdmin):
	pass
admin.site.register(TopNews, TopNewsAdmin)