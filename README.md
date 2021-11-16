# Green Mountain Power

This is an unofficial Python client that uses the undocumented API for Green Mountain Power accounts.

## Quickstart

To start using this client, install it using pip.

```sh
pip3 install greenmountainpower
```

And then import the client and use it to fetch usage data.

```python
import datetime
import greenmountainpower

print("Collecting usage...")

gmp = greenmountainpower.api.GreenMountainPowerApi(
    account_number=58504395849, username="jsmith", password="mypassword"
)

now = datetime.datetime.now()
one_day_ago = now - datetime.timedelta(days=1)
usages = gmp.get_usage(
    precision=greenmountainpower.api.UsagePrecision.HOURLY,
    start_time=one_day_ago,
    end_time=now,
)

for usage in usages:
    print(f" - Time: {usage.start_time.isoformat()}, Usage: {usage.consumed_kwh} KWH")

```

Output:

```
Collecting usage...
 - Time: 2021-11-14T01:00:00, Usage: 0.27 KWH
 - Time: 2021-11-14T02:00:00, Usage: 0.22 KWH
 - Time: 2021-11-14T03:00:00, Usage: 0.24 KWH
 - Time: 2021-11-14T04:00:00, Usage: 0.25 KWH
 - Time: 2021-11-14T05:00:00, Usage: 0.26 KWH
 - Time: 2021-11-14T06:00:00, Usage: 0.26 KWH
 ...
```

## Publishing

To publish a new version, follow these steps.

```sh
git tag <version> # ensure all changes are committed
python3 -m build # build the package
twine upload --repository pypi dist/*
```
