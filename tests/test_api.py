import datetime
import pytest

from unittest.mock import patch

from greenmountainpower.api import (
    GreenMountainPowerApi,
    Usage,
    _BASE_URL,
    AccountStatus,
)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs.get("url") == f"{_BASE_URL}/api/v2/accounts/123456/status":
        return MockResponse({"accountNumber": "123456"}, 200)

    return MockResponse(None, 404)


@pytest.fixture
@patch("greenmountainpower.api.requests_oauthlib.OAuth2Session.fetch_token")
def client(mock_fetch_token):
    return GreenMountainPowerApi(
        account_number=123456, username="user", password="pass"
    )


def test_try_parse_data():
    data = {"date": "2022-01-01T00:00:00Z", "consumed": 10.5}
    result = list(Usage.try_parse_data(data))
    assert len(result) == 1
    assert isinstance(result[0], Usage)
    assert result[0].start_time == datetime.datetime(2022, 1, 1, 0, 0, 0)
    assert result[0].consumed_kwh == 10.5


def test_instantiate_client(client):
    assert client.account_number == 123456


@patch(
    "greenmountainpower.api.requests_oauthlib.OAuth2Session.get",
    side_effect=mocked_requests_get,
)
def test_get_account_status(mock_get, client):
    res = client.get_account_status()
    assert res == AccountStatus(accountNumber="123456")
