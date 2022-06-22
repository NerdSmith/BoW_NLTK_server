from django.contrib import admin
from .models import Post, BoW


class BoWAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Post)
admin.site.register(BoW, BoWAdmin)