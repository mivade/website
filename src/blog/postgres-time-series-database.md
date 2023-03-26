---
title: Using Postgres as a time series database
date: 2016-06-25
tags:
  - postgres
  - sql
  - pandas
  - python
  - data
---

Time series databases (TSDBs) are quite popular these days. To name a
few, there are [InfluxDB][], [Graphite][], [Druid][], [Kairos][], and
[Prometheus][]. All aim to optimize data storage and querying for
time-based data, which is highly relevant in a physics labs where
there are multitude of "metrics" (to borrow a phrase used frequently
in TSDB documentation) that naturally lend themselves to time series
representation: lab (and individual device) temperatures, vacuum
chamber pressures, and laser powers, just to name a few. Ideally, one
could log various data to one of these databases and then use a tool
like [Grafana][] to visualize it. Sadly, more traditional relational
databases like [SQLite][] and [PostgreSQL][] are not (currently)
supported by Grafana (although this is now being addressed by a
datasource plugin in development).

Nevertheless, there are quite a few reasons to favor a traditional
RDBMS over a newfangled TSDB. To name a few:

* Longevity: SQL has been around since the 1970s and became
  standardized in the 1980s.
* Ubiquity: almost every server (web or otherwise) has an instance of
  SQL installed. If not, SQLite doesn't even require a server!
* Community: not to suggest there aren't good communities with TSDBs,
  but the Postgres and SQLite communities in particular are generally
  quite helpful.  Combined with the longevity aspect, any question one
  may have about how to accomplish a particular task with a SQL
  database is likely to be easily answerable with a simple web search.

In this post, I will outline a few things I have learned in using SQL
for storing time series data. In particular, I will focus on Postgres,
but the same general principles apply to other dialects. Sample code for
some examples can be found on [GitLab](https://gitlab.com/mivade/postgres-timeseries).

[InfluxDB]: https://influxdata.com/time-series-platform/influxdb/
[Graphite]: https://graphite.readthedocs.io/en/latest/
[Druid]: http://druid.io/
[Kairos]: https://kairosdb.github.io/
[Prometheus]: https://prometheus.io/
[Grafana]: http://grafana.org/
[SQLite]: https://sqlite.org/
[PostgreSQL]: https://www.postgresql.org/

## Schema definition

One "disadvantage" to SQL is it traditionally requires tightly defined
schema.  In practice when logging time series data, this is not
usually a problem since each measurement device can neatly have its
own column. Where this can become somewhat of nuiscance is when adding
new devices. InfluxDB (for example) gets around this with its query
language being quite flexible. In traditional SQL, the approach would
require altering a table to add a new column. This is not too
difficult in principle, but requires a (naive) program for logging
data to frequently make `ALTER TABLE` calls and check if columns
already exist. (Note that if using Python, this can be easily dealt
with by using the [dataset][] library.).

In real laboratories, though, we tend to know the kinds of things we
are going to measure. So even if we add new devices that we want to
log data from, we can still come up with a reasonable schema
definition that fits well within the SQL paradigm. As an example,
let's consider storing data from thermocouples in a table. We could
get away with as few as three columns to describe the data: a
timestamp (of course), a name or unique ID of the sensor, and a
temperature measurement. For good measure, we should also add a
primary key ID column to make a grand total of four columns. So far,
our table looks like this:

```
 id |           timestamp           |  sensor   | temperature
----+-------------------------------+-----------+-------------
```

For the `timestamp` column, I highly recommend using `TIMESTAMP WITH
TIME ZONE` rather than `TIMESTAMP WITHOUT TIME ZONE` (more on why
later).

For efficient querying, we'll want to index the `timestamp` and
`sensor` columns. Depending on the number of sensors, it may also make
sense to make a combined index on both, but we can defer this decision
to later if it becomes necessary. Using [SQLAlchemy][], we define our
table like this:

```python
metadata = sa.MetaData()
table = sa.Table(
    'timeseries', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('timestamp', sa.DateTime(timezone=True),
              nullable=False, index=True),
    sa.Column('sensor', sa.String(length=128), nullable=False, index=True),
    sa.Column('temperature', sa.Float(precision=4), nullable=False))
metadata.create_all(bind=engine)
```

which results in the following SQL:

```pgsql
CREATE TABLE timeseries (
	id SERIAL NOT NULL,
	timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
	sensor VARCHAR(128) NOT NULL,
	temperature FLOAT(4) NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX ix_timeseries_sensor ON timeseries (sensor);
CREATE INDEX ix_timeseries_timestamp ON timeseries (timestamp);
```

[SQLAlchemy]: http://www.sqlalchemy.org/
[dataset]: https://dataset.readthedocs.io/en/latest/

## Basic querying

Simple queries are performed as normal:

```pgsql
SELECT * FROM timeseries WHERE sensor = 'sensor_01';
```

Postgres has quite a few
[date and time functions](https://www.postgresql.org/docs/9.1/static/functions-datetime.html)
for building more complicated queries. It understands [ISO 8601][] out
of the box:

```pgsql
test=> SELECT * FROM timeseries
test-> WHERE timestamp > '2016-06-13T22:00+02'
test-> AND sensor = 'sensor_01';
 id |           timestamp           |  sensor   | temperature
----+-------------------------------+-----------+-------------
  8 | 2016-06-14 23:18:16.149606+02 | sensor_01 |     22.7061
  4 | 2016-06-14 23:18:11.985645+02 | sensor_01 |     25.4643
(2 rows)
```

Here we are explicit with the UTC offset of +2 hours (CEST). If
omitted, the server locale is assumed. This brings us to why we should
bother with time zones in the first place: internally, we want all
timestamps stored in UTC to avoid ambiguity (Postgres already does
this internally). Externally, (e.g., from Python scripts), we want to
be able to use whatever time zone we're in to not have to think too
hard.

SQLAlchemy treats naive `datetime` objects, uh, naively. This means
that if a new `datetime` is created without explicitly specifying a
time zone, that +2 hours above is lost and our time quries will start
to get confusing. To avoid this problem, the best solution I have
found is to **always** declare columns as `TIMESTAMP WITH TIME ZONE`
(`DateTime(timezone=True)` in SQLAlchemy terms) and explicitly. So
rather than inserting new timestamps with

```python
from datetime import datetime
# ...
timestamp = datetime.now()
```

instead prefer

```python
from datetime import datetime, timezone
# ...
timestamp = datetime.now(timezone.utc)
```

*Aside: why oh why doesn't `datetime.utcnow` just do this?*

Now we can build queries in Python like this using pandas and raw SQL
queries:

```python
today = datetime.now(timezone.utc)
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
query = (
    "SELECT * FROM timeseries " +
    "WHERE timestamp >= '{}' ".format(today.isoformat()) +
    "AND sensor = 'sensor_01'"
)
df = pd.read_sql_query(query, engine, index_col="timestamp")
```

[ISO 8601]: https://en.wikipedia.org/wiki/ISO_8601

## Data aggregation

Depending on data density, it may be useful to downsample data and look
at aggregates such as the mean temperature in half-hour windows over the
course of a day. We can easily accomplish this after the fact with
pandas, but we can just as easily use Postgres [aggregate functions][]
to do this for us on the server. One advantage to this approach is a
reduction in network overhead, which is especially relevant for very
large datasets. Another is that these queries can be cached using
[materialized views][]. (This is a more advanced topic that I will not
cover here. Instead, see the link in the references section below for a
good treatment).

The key here is to use the `date_trunc` aggregate function and
`GROUP BY` to only look at (for example) one hour at a time. An example
of an aggregate query:

```pgsql
SELECT
  date_trunc('hour', timestamp) AS timestamp,
  avg(temperature) AS temperature
FROM timeseries
WHERE timestamp >= '2016-06-25'
AND sensor = 'sensor_01'
GROUP BY date_trunc('hour', timestamp)
ORDER BY timestamp;
```

which results in something like:

```
timestamp        |   temperature
------------------------+------------------
2016-06-25 00:00:00+02 | 22.0828623312065
2016-06-25 01:00:00+02 | 22.0026334276975
2016-06-25 02:00:00+02 | 21.9871146672498
2016-06-25 03:00:00+02 | 22.0274553065207
2016-06-25 04:00:00+02 | 21.9357200048187
2016-06-25 05:00:00+02 | 21.9737668623899
2016-06-25 06:00:00+02 | 22.0098525849685
2016-06-25 07:00:00+02 | 22.0767008988982
2016-06-25 08:00:00+02 | 22.2146511332874
2016-06-25 09:00:00+02 | 21.9118559617263
2016-06-25 10:00:00+02 | 22.0417969508838
2016-06-25 11:00:00+02 | 22.0554379473676
2016-06-25 12:00:00+02 | 22.0193907419841
2016-06-25 13:00:00+02 | 22.0560295554413
2016-06-25 14:00:00+02 | 21.8087244594798
2016-06-25 15:00:00+02 | 22.0494429762518
2016-06-25 16:00:00+02 | 21.9082782661007
2016-06-25 17:00:00+02 | 21.4403478373652
(18 rows)
```

[aggregate functions]: https://www.postgresql.org/docs/current/static/functions-aggregate.html
[materialized views]: https://www.postgresql.org/docs/current/static/rules-materializedviews.html

## Other strategies

Another approach to avoid the time zone issue entirely is to simply
store timestamps using something like UNIX time. Since pretty much every
programming language imaginable has a built-in function to return time
in seconds since the epoch, this is a reasonable approach (and is a bit
more portable to other SQL dialects). The major downside to this is that
compared to ISO 8601, UNIX time is not as readable by humans and
therefore may require extra steps to convert to and from a human-readable
format.

Depending on what you are doing with your data, it could also make sense
to store, say, an hour's worth of data in a single row using the `ARRAY`
data type. Combining arrays with [array functions][] could then
effectively do aggregation (somewhat) automatically rather than by
query. This could also mean a bit of extra work when inserting new data
or getting data stored in the database into a form friendly to your data
analysis tools of choice.

[array functions]: https://www.postgresql.org/docs/9.1/static/functions-array.html

## References and further reading

* [Querying Time Series in Postgresql](https://no0p.github.io/postgresql/2014/05/08/timeseries-tips-pg.html)
* [Materialized View Strategies Using PostgreSQL](https://hashrocket.com/blog/posts/materialized-view-strategies-using-postgresql)
