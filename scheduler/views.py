from django.db.models.query import QuerySet
from scheduler.models import ScheduledRequest
from scheduler.tables import ScheduledRequestTable
from django.views.generic import TemplateView
from django_tables2 import SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    """Landing page"""
    template_name = "scheduler/home.html"


class AboutView(TemplateView):
    """Basic information about the project"""
    template_name = "scheduler/about.html"


class ScheduleView(LoginRequiredMixin, SingleTableView):
    """View that returns the list of ScheduledRequests created by the user"""
    model = ScheduledRequest
    table_class = ScheduledRequestTable
    template_name = "scheduler/schedule.html"

    def get_queryset(self) -> QuerySet:
        return ScheduledRequest.objects.filter(user=self.request.user).all()
