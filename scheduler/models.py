from django.db import models
from accounts.models import CustomUser


class ScheduledRequestType(models.TextChoices):
    GET = "GET", "GET"
    HEAD = "HEAD", "HEAD"
    POST = "POST", "POST"
    PUT = "PUT", "PUT"
    DELETE = "DELETE", "DELETE"
    CONNECT = "CONNECT", "CONNECT"
    OPTIONS = "OPTION", "OPTION"
    TRACE = "TRACE", "TRACE"
    PATCH = "PATCH", "PATCH"


class ScheduledRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILURE = "FAILURE", "Failure"


class ScheduledRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_type = models.CharField(
        "Request type",
        choices=ScheduledRequestType.choices,
        default=ScheduledRequestType.GET,
        max_length=20,
    )
    url = models.URLField("URL")
    headers = models.TextField(
        "Headers",
        help_text="Please use key:value pairs, one header per line",
        null=True,
        blank=True,
    )
    params = models.TextField(
        "URL parameters",
        help_text="Specify the URL parameters to be used for the request, please use key:value pairs, one header per line",
        null=True,
        blank=True,
    )
    data = models.TextField(
        "Data",
        help_text="Data submitted in the body payload, please use key:value pairs, one header per line",
        null=True,
        blank=True,
    )
    scheduled_time = models.DateTimeField("Scheduled time", db_index=True)
    response = models.TextField("Response data", null=True)
    request_status = models.CharField(
        "Status",
        choices=ScheduledRequestStatus.choices,
        default=ScheduledRequestStatus.PENDING,
        max_length=20,
    )
