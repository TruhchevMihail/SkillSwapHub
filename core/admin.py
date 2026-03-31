from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'actor', 'action', 'content_type', 'object_id', 'created_at')
    list_filter = ('action', 'created_at', 'content_type')
    search_fields = ('actor__username', 'note')
    readonly_fields = ('created_at',)

