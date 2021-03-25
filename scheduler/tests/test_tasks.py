import pytest
from scheduler.models import ScheduledRequest, ScheduledRequestStatus
from scheduler.management.commands.run_scheduler import handle_scheduled_requests
from unittest import mock
import requests_mock


@pytest.mark.django_db
def test_scheduler_executes_requests(freezer, scheduled_requests_same_time):
    assert ScheduledRequest.objects.filter(
        request_status=ScheduledRequestStatus.PENDING
    ).count() == 2
    freezer.move_to("2021-01-01-12-00")
    handle_scheduled_requests()
    assert ScheduledRequest.objects.filter(
        request_status=ScheduledRequestStatus.SUCCESS
    ).count() == 2


@pytest.mark.django_db
def test_scheduler_doesnt_execute_requests_before_their_schedule(freezer, scheduled_requests_different_time):
    freezer.move_to("2021-01-01-12-00")
    handle_scheduled_requests()
    assert ScheduledRequest.objects.filter(
        request_status=ScheduledRequestStatus.SUCCESS
    ).count() == 1


@pytest.mark.django_db
def test_malformed_input_causes_request_to_go_through(freezer, scheduled_request_malformed_input):
    freezer.move_to("2021-01-01-12-00")
    handle_scheduled_requests()
    assert ScheduledRequest.objects.filter(
        request_status=ScheduledRequestStatus.SUCCESS
    ).count() == 1


@mock.patch('requests.get', mock.Mock(side_effect=lambda: Exception('Error!')))
@pytest.mark.django_db
def test_failure_has_appropriate_status(freezer, scheduled_request):
    freezer.move_to("2021-01-01-12-00")
    handle_scheduled_requests()
    assert ScheduledRequest.objects.filter(
        request_status=ScheduledRequestStatus.FAILURE
    ).count() == 1


@pytest.mark.django_db
def test_scheduled_request_with_headers_params_body(freezer, scheduled_request_with_additional_info):
    with requests_mock.mock() as m:
        m.get('http://example.com', text='response') 
        freezer.move_to("2021-01-01-12-00")
        handle_scheduled_requests()
    
    req = m.last_request
    assert req.headers['one'] == 'two' and req.headers['three'] == 'four'
    assert req.url == "http://example.com/?five=six&seven=eight"
    assert 'nine=ten&one=two' in req.body
