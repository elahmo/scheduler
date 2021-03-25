import pytest
from scheduler.models import ScheduledRequest, ScheduledRequestType
from datetime import datetime
from accounts.models import CustomUser


@pytest.fixture
def user():
    user = CustomUser.objects.create(email="test@test.com", password="Pwd123!")
    return user


@pytest.fixture
def scheduled_request(user):
    req = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
    )
    return req


@pytest.fixture
def scheduled_request_with_additional_info(user):
    req = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
        headers="one:two\nthree:four",
        params="five:six\nseven:eight",
        data="nine:ten\none:two",
    )
    return req


@pytest.fixture
def scheduled_requests_same_time(user):
    req_one = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
    )
    req_two = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
    )
    return [req_one, req_two]


@pytest.fixture
def scheduled_requests_different_time(user):
    req_one = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
    )
    req_two = ScheduledRequest.objects.create(
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 13, 00),
    )
    return [req_one, req_two]


@pytest.fixture
def scheduled_request_malformed_input(user):
    req = ScheduledRequest.objects.create(
        params="something wrong",
        user=user,
        url="http://example.com",
        request_type=ScheduledRequestType.GET,
        scheduled_time=datetime(2021, 1, 1, 12, 00),
    )
    return req
