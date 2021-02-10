from django.contrib import admin
from .models import Pattern, Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = [
        'pattern_title',
        'pattern_content',
        'message',
        'created_on',
    ]

    list_display_links = None

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Pattern)
admin.site.register(Entry, EntryAdmin)
