from greenmountainpower.api import Usage, GreenMountainPowerApi
from unittest.mock import patch
import datetime


def test_try_parse_data():
    data = {
        "date": "2022-01-01T00:00:00Z",
        "consumed": 10.5
    }
    result = list(Usage.try_parse_data(data))
    assert len(result) == 1
    assert isinstance(result[0], Usage)
    assert result[0].start_time == datetime.datetime(2022, 1, 1, 0, 0, 0)
    assert result[0].consumed_kwh == 10.5

@patch("greenmountainpower.api.requests_oauthlib.OAuth2Session")
def test_instantiate_client(mock_oauth2_session):
    account_number = 12345
    username = "test"
    password = "test"
    g = GreenMountainPowerApi(account_number, username, password)
    assert g.account_number == account_number
