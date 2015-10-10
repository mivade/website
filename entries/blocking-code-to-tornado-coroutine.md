title: Running (possibly) blocking code like a Tornado coroutine
date: 2015-08-03 19:54
tags: python, tornado, async

One of the main benefits of using the
[Tornado](http://www.tornadoweb.org/en/stable/) web server is that it is
(normally) a single-threaded, asynchronous framework that can rely on
coroutines for concurrency. Many drivers already exist to provide a
client library utilizing the Tornado event loop and coroutines (e.g.,
the [Motor](https://github.com/mongodb/motor/)
[MongoDB](https://www.mongodb.org/) driver).

To write your own coroutine-friendly code for Tornado, there are a few
different options available, all requiring that you somehow wrap
blocking calls within a Future so as to allow the event loop to continue
executing. Here, I demonstrate one recipe to do just this by utilizing
`Executor` objects from the `concurrent.futures` module. We start with
the imports:

```python
import random
import time
from tornado import gen
from tornado.concurrent import run_on_executor, futures
from tornado.ioloop import IOLoop
```

> **note**
>
> `concurrent.futures` is standard in Python \>= 3.2 and is
> :   installable via `pip install futures` for older versions.
>

We will be using the `run_on_executor` decorator which requires that the
class whose methods we decorate have some type of `Executor` attribute
(the default is to use the `executor` attribute, but a different
`Executor` can be used with a keyword argument passsed to the
decorator). We'll create a class to run our asynchronous tasks and give
it a `ThreadPoolExecutor` for executing tasks. In this contrived
example, our long running task just sleeps for a random amont of time:

```python
class TaskRunner(object):
    def __init__(self, loop=None):
        self.executor = futures.ThreadPoolExecutor(4)
        self.loop = loop or IOLoop.instance()

    @run_on_executor
    def long_running_task(self):
        tau = random.randint(0, 3)
        time.sleep(tau)
        return tau
```

Now, from within a coroutine, we can let the tasks run as if they were
normal coroutines:

```python
loop = IOLoop() # this is necessary if running as an ipynb!
tasks = TaskRunner(loop)

@gen.coroutine
def do_stuff():
    result = yield tasks.long_running_task()
    raise gen.Return(result)

def do_other_stuff():
    print(random.random())
```

Finally, in the main coroutine:

```python
@gen.coroutine
def main():
    for i in range(10):
        stuff = yield do_stuff()
        print(stuff)
        do_other_stuff()

loop.run_sync(main)
```

Which produces output like:

Using this general pattern, it is rather easy to adapt blocking calls to
Tornado's coroutines. Note that the example code can be found
[here](https://gist.github.com/mivade/5966f1b7a995a50ecc55).
