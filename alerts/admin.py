# alerts/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Alert  # import your model


class AlertAdmin(admin.ModelAdmin):
    list_display = ("violation_type", "camera_id", "summary", "snapshot_preview")
    readonly_fields = ("snapshot_preview", "summary")  # make summary read-only in admin

    def snapshot_preview(self, obj):
        if obj.snapshot:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="200" />',
                obj.snapshot.url,
                obj.snapshot.url,
            )
        return "(No image)"

    snapshot_preview.short_description = "Snapshot Preview"


# ✅ Only register once
admin.site.register(Alert, AlertAdmin)
