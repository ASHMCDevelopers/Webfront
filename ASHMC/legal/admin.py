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
