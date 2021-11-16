import dataclasses
import datetime
import enum

import oauthlib
import requests_oauthlib

from . import exceptions

_CLIENT_ID = "C95D19408B024BD4BEB42FA66F08BCEA"

_BASE_URL = "https://api.greenmountainpower.com"


@dataclasses.dataclass
class Usage:
    start_time: datetime.datetime
    consumed_kwh: float

    @classmethod
    def try_parse_data(cls, data: dict):
        try:
            yield cls(
                start_time=datetime.datetime.strptime(
                    data["date"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                consumed_kwh=data["consumed"],
            )
        except KeyError:
            pass


class UsagePrecision(enum.Enum):
    MONTHLY = "monthly"
    DAILY = "daily"
    HOURLY = "hourly"


class GreenMountainPowerApi:
    """Client for accessing Green Mountain Power API"""

    def __init__(self, account_number: int, username: str, password: str):
        self.account_number = account_number

        def token_updater(token):
            self.session.token = token

        self.session = requests_oauthlib.OAuth2Session(
            client=oauthlib.oauth2.LegacyApplicationClient(client_id=_CLIENT_ID),
            auto_refresh_url=f"{_BASE_URL}/api/v2/applications/token",
            token_updater=token_updater,
        )
        token = self.session.fetch_token(
            token_url=f"{_BASE_URL}/api/v2/applications/token",
            username=username,
            password=password,
            include_client_id=True,
            force_querystring=True,
        )

    def get_usage(
        self,
        precision: UsagePrecision,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ):
        response = self.session.get(
            url=f"{_BASE_URL}/api/v2/usage/{self.account_number}/{precision.value}",
            params={
                "startDate": start_time.astimezone().isoformat(),
                "endDate": end_time.astimezone().isoformat(),
            },
        )
        if response.status_code == 400:
            raise exceptions.BadRequestException(response.json()["message"])
        if response.status_code == 401:
            raise exceptions.UnauthorizedException(response.json()["message"])
        data = response.json()
        return [
            usage
            for interval in data["intervals"]
            for value in interval["values"]
            for usage in Usage.try_parse_data(value)
        ]
