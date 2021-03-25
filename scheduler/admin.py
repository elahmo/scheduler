from django.contrib import admin
from scheduler.models import ScheduledRequest


@admin.register(ScheduledRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("url", "request_type", "scheduled_time", "request_status")
    list_filter = ("request_type", "request_status")
    exclude = ("user", "request_status")
    readonly_fields = ("response",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "request_type",
                    "url",
                    "headers",
                    "params",
                    "data",
                    "scheduled_time",
                )
            },
        ),
        (
            "Response data",
            {
                "classes": ("collapse",),
                "fields": ("response",),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_module_permission(self, request):
        if request.user.is_staff:
            return True
        return super().has_module_permission(request)

    def has_add_permission(self, request):
        if request.user.is_staff:
            return True
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_change_permission(request, obj=None)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return super().has_delete_permission(request, obj=None)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
