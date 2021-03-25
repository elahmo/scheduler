from django.utils.html import format_html
import django_tables2 as tables
from .models import ScheduledRequest


class ScheduledRequestTable(tables.Table):
    url = tables.Column()

    class Meta:
        model = ScheduledRequest
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "url",
            "request_type",
            "scheduled_time",
            "request_status",
        )

    BADGE_MAPPING = {
        "Pending": "secondary",
        "Success": "success",
        "Failure": "danger",
    }

    def render_request_status(self, value):
        return format_html(
            '<span class="badge badge-pill badge-{}">{}</span>',
            self.BADGE_MAPPING[value],
            value,
        )
