---
title: Background tasks with Tornado
date: 2015-02-28
tags:
  - python
  - tornado
  - lab
---

I have been using [Tornado][] lately for distributed control of
devices in the lab where an asynchronous framework is advantageous. In
particular, we have a [HighFinesse][] [wavelength meter][wavemeter]
which we use to monitor and stabilize several lasers (up to 14 at a
time). Previously, a custom server for controlling this wavemeter was
written using [Twisted][], but that has proven difficult to upgrade,
distribute, and maintain.

One thing that is common for such a control scenario is that data
needs to be refreshed continuously while still allowing incoming
connections from clients and appropriately executing remote procedure
calls. One method would be to periodically interrupt the Tornado IO
loop to refresh data (and in fact, Tornado has a class to make this
easy for you in `tornado.ioloop.PeriodicCallback`). This can be fine
if the data refreshing does not take too much time, but all other
operations will be blocked until the callback is finished, which can
be a problem if the refreshing operation is slow. Another option is to
have an additional thread separate from the Tornado IO loop that
handles refreshing data. This certainly works, but adds the complexity
of needing to use thread-safe communications to stop the thread when
the main application is shut down or when other tasks depend on the
successful completion of the refresh.

Luckily, Tornado also includes a decorator,
`tornado.concurrent.run_on_executor`, to run things in the background
for you using Python's `concurrent.futures` module (which is standard
starting in Python 3.3 and backported for other versions). Then
instead of writing the refresh function as a loop that runs in the
background, you instead have its final call be to add itself back as a
callback on the IO loop. This makes shutdown trivial since only the IO
loop needs to be stopped when the program is closed. A refresh
function could thus look something like this:

```python
@tornado.concurrent.run_on_executor
def refresh():
    do_something_that_takes_a_while()
	tornado.ioloop.IOLoop.instance().add_callback(self.refresh)
```

Now after `refresh` is called once, it will continuously run until the
IO loop is stopped.

For a more complete example, I have written a small [demo][].

[Tornado]: http://www.tornadoweb.org/en/stable/
[HighFinesse]: http://www.highfinesse.com/
[wavemeter]: http://www.highfinesse.com/en/wavelengthmeter/
[Twisted]: https://twistedmatrix.com/trac/
[demo]: https://gist.github.com/mivade/421c427db75c8c5fa1d1
