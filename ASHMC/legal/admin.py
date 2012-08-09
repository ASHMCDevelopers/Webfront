from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import *


class ArticleAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, article, form, change):
        """Keep track of who modified this object."""
        article.save()
        mod = Modification.objects.create(
            user=request.user,
            article=article,
        )

        article.modification_set.add(mod)

admin.site.register(Article, ArticleAdmin)


class ModificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Modification, ModificationAdmin)


class OfficialFormAdmin(admin.ModelAdmin):
    def get_file_path(obj):
        return obj.file_actual.path
    def get_file_url(obj):
        return obj.file_actual.url
    list_display = ('__unicode__', get_file_path, get_file_url)
    list_filter = ('last_updated',)
admin.site.register(OfficialForm, OfficialFormAdmin)


class GDocSheetAdmin(admin.ModelAdmin):
    pass
admin.site.register(GDocSheet, GDocSheetAdmin)
