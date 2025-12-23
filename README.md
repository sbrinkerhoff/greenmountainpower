# Green Mountain Power

This is an unofficial Python client that uses the undocumented API for [Green Mountain Power](https://greenmountainpower.com) accounts.  Green Mountain Power is a energy utility located in Vermont, USA.

## Usage Data

This client was written primarily to download usage (and generation) data from the Green Mountain Power API that powers the official [account dashboard](https://greenmountainpower.com/account/).  This data appears to be uploaded each morning at 4AM ET and contains the previous days data upto `4AM EST`.  The `4AM EST` time bucket appears in the dataset, but is incomplete.  It would appear the usage (and generation) data from the API should only be used for the previous days completed calendar days data and not expected to contain the current days data.

```
Current Date: 2025-12-23

...
 - Time: 2025-12-22T22:00:00, Usage: 0.24 KWH, Generation: None
 - Time: 2025-12-22T23:00:00, Usage: 0.24 KWH, Generation: None
 - Time: 2025-12-23T00:00:00, Usage: 0.2 KWH, Generation: None
 - Time: 2025-12-23T01:00:00, Usage: 0.2 KWH, Generation: None
 - Time: 2025-12-23T02:00:00, Usage: 0.19 KWH, Generation: None
 - Time: 2025-12-23T03:00:00, Usage: 0.19 KWH, Generation: None
 - Time: 2025-12-23T04:00:00, Usage: 0.04 KWH, Generation: None <<< incomplete data
```

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
