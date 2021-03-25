# runapscheduler.py
from datetime import datetime, timedelta
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import requests

from scheduler.models import ScheduledRequest, ScheduledRequestStatus


logger = logging.getLogger(__name__)


def handle_scheduled_requests():
    logger.info("Performing task")
    _time = datetime.utcnow()
    current_time = datetime(
        _time.year, _time.month, _time.day, _time.hour, _time.minute
    )
    # get the requests that are scheduled for this minute
    scheduled_requests = ScheduledRequest.objects.filter(
        scheduled_time__gte=current_time,
        scheduled_time__lte=current_time + timedelta(minutes=1),
    )
    logger.info(f"Found {scheduled_requests.count()} requests")
    for scheduled_request in scheduled_requests:
        try:
            url = scheduled_request.url
            request_type = scheduled_request.request_type
            request_kwargs = {}

            for request_attr in ["headers", "params", "data"]:
                try:
                    if getattr(scheduled_request, request_attr):
                        attributes = {}
                        for line in getattr(
                            scheduled_request, request_attr
                        ).splitlines():
                            key, value = line.split(":")
                            attributes[key] = value
                        request_kwargs[request_attr] = attributes
                except ValueError:
                    continue

            response = getattr(requests, request_type.lower())(
                url=url, **request_kwargs
            )

            if response.ok:
                scheduled_request.request_status = ScheduledRequestStatus.SUCCESS
            else:
                scheduled_request.request_status = ScheduledRequestStatus.FAILURE

            scheduled_request.response = response.text
        except:
            logger.warning("Something went wrong:", exc_info=True)
            scheduled_request.request_status = ScheduledRequestStatus.FAILURE
        scheduled_request.save()


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            handle_scheduled_requests,
            trigger=CronTrigger(minute="*/1"),
            id="handle_scheduled_requests",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
