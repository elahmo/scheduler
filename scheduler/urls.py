from django.urls import path
from scheduler import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("schedule/", views.ScheduleView.as_view(), name="schedule"),
    path("about/", views.AboutView.as_view(), name="about"),
]
