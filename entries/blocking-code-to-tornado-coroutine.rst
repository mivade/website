:title: Running (possibly) blocking code like a Tornado coroutine
:date: 2015-08-03 19:54
:tags: python, tornado, async

One of the main benefits of using the Tornado_ web server is that it
is (normally) a single-threaded, asynchronous framework that can rely
on coroutines for concurrency. Many drivers already exist to provide a
client library utilizing the Tornado event loop and coroutines (e.g.,
the Motor_ MongoDB_ driver).

.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _Motor: https://github.com/mongodb/motor/
.. _MongoDB: https://www.mongodb.org/

To write your own coroutine-friendly code for Tornado, there are a few
different options available, all requiring that you somehow wrap
blocking calls within a Future so as to allow the event loop to
continue executing. Here, I demonstrate one recipe to do just this by
utilizing ``Executor`` objects from the ``concurrent.futures``
module. We start with the imports:

.. code-block:: python

    import random
    import time
    from tornado import gen
    from tornado.concurrent import run_on_executor, futures
    from tornado.ioloop import IOLoop

.. note:: ``concurrent.futures`` is standard in Python >= 3.2 and is
          installable via ``pip install futures`` for older versions.

We will be using the ``run_on_executor`` decorator which requires that
the class whose methods we decorate have some type of ``Executor``
attribute (the default is to use the ``executor`` attribute, but a
different ``Executor`` can be used with a keyword argument passsed to
the decorator). We'll create a class to run our asynchronous tasks and
give it a ``ThreadPoolExecutor`` for executing tasks. In this
contrived example, our long running task just sleeps for a random
amont of time:

.. code-block:: python

    class TaskRunner(object):
        def __init__(self, loop=None):
            self.executor = futures.ThreadPoolExecutor(4)
            self.loop = loop or IOLoop.instance()
        
        @run_on_executor
        def long_running_task(self):
            tau = random.randint(0, 3)
            time.sleep(tau)
            return tau

Now, from within a coroutine, we can let the tasks run as if they were
normal coroutines:

.. code-block:: python

    loop = IOLoop() # this is necessary if running as an ipynb!
    tasks = TaskRunner(loop)
    
    @gen.coroutine
    def do_stuff():
        result = yield tasks.long_running_task()
        raise gen.Return(result)
        
    def do_other_stuff():
        print(random.random())

Finally, in the main coroutine:

.. code-block:: python

    @gen.coroutine
    def main():
        for i in range(10):
            stuff = yield do_stuff()
            print(stuff)
            do_other_stuff()
    
    loop.run_sync(main)

Which produces output like:

.. parsed-literal::

    3
    0.6012166386789509
    1
    0.9235652108721132
    0
    0.42316507955015026
    3
    0.9766563871068523
    1
    0.21032495467534018
    2
    0.15572313672917715
    0
    0.8767039780374377
    3
    0.6542727048597389
    2
    0.3623342196737247
    0
    0.30042493880819876


Using this general pattern, it is rather easy to adapt blocking calls
to Tornado's coroutines. Note that the example code can be found
here__.

__ https://gist.github.com/mivade/5966f1b7a995a50ecc55

