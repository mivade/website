---
title: Ensuring timestamp storage in UTC with SQLAlchemy
date: 2019-03-29
tags:
  - python
  - sql
  - sqlalchemy
  - notes
---

Naively one might think that using defining a column with
`DateTime(timezone=True)` when defining a SQL table with
[SQLAlchemy](https://www.sqlalchemy.org/) would result in a timezone-aware
`datetime` object when loading into Python from the database. This doesn't
always work however, in particular when using SQLite. Note the following
behavior:

```python
from datetime import datetime, timezone
import sqlalchemy as sa

engine = sa.create_engine("sqlite:///")
metadata = sa.MetaData()
bad_datetimes = sa.Table(
    "bad_datetimes", metadata,
    sa.Column("datetime", sa.DateTime(timezone=True))
)
metadata.create_all(bind=engine)

# Try inserting both a naive datetime and a timezone-aware datetime
engine.execute(bad_datetimes.insert().values([
    {"datetime": datetime.now()},
    {"datetime": datetime.now(timezone.utc)}
]))

print(engine.execute(bad_datetimes.select()).fetchall())

# Results in:
# [(datetime.datetime(2019, 3, 29, 13, 56, 1, 224546),), (datetime.datetime(2019, 3, 29, 19, 56, 1, 224554),)]
```

So despite telling `DateTime` that we want timezones, that information has been
lost!

To resolve this behavior, we can use `sa.types.TypeDecorator` to always get
timezone-aware datetimes:

```python
class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo

    def process_bind_param(self, value: datetime, dialect):
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(timezone.utc)

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

good_datetimes = sa.Table(
    "good_datetimes", metadata,
    sa.Column("datetime", TimeStamp())
)
metadata.create_all(bind=engine)

engine.execute(good_datetimes.insert().values([
    {"datetime": datetime.now()},
    {"datetime": datetime.now(timezone.utc)}
]))
print(engine.execute(good_datetimes.select()).fetchall())

# Results in:
# [(datetime.datetime(2019, 3, 29, 20, 1, 10, 718427, tzinfo=datetime.timezone.utc),),
#  (datetime.datetime(2019, 3, 29, 20, 1, 10, 718431, tzinfo=datetime.timezone.utc),)]
```

Note that in this example we're assuming that naive datetimes are always in the
local timezone. This may not always be the right assumption, in which case we
would probably want to just enforce the usage of timezone-aware `datetime`s in
the first place.
