:title: Distributed computing with Celery
:date: 2015-08-06
:tags: python, celery
:status: draft

Python, although an interpreted language, remains reasonably fast for
numerical computations via Numpy_ and related libraries thanks to
their compiled cores. This allows certain operations to be executed at
near-native speed; close enough, in many cases, that there are no
significant gains to using a compiled language like C directly. That
is, provided for loops can be avoided in favor of Numpy array slicing
expressions. Unfortunately, for loops can't always be avoided for
`embarrassingly parallel`_ problems such as `Monte Carlo
simulations`_.

Thankfully, modern PCs usually have multiple cores, and with
networking, the number of available cores to tackle an embarrassingly
parallel problem can increase rapidly. A number of tools exist for
parallel processing in Python: the standard library's
``multiprocessing`` module or the parallel computing architecture of
IPython_, among others. IPython's parallel computing model is
exceptional, but it suffers from being rather complex to get things
setup on multiple computers or even for having the right things
imported.

Another tool which makes parallel computing with small, ad hoc
clusters is Celery_. Celery is a distributed task queue which is
commonly used among web developers to offload potentially long-running
tasks from web servers which can then focus on responding to requests
as quickly as they come in. A simplistic overview of using Celery for
parallel computing is as follows:

* A central script (let's call it the hub) decides what parallel
  computations need to be performed and submits these tasks in chunks
  to a centralized message broker.
* A number of workers are deployed on as many computers as are
  available that can talk to the broker. The workers crunch the
  numbers and store their results in a configured results backend.
* The hub aggregates the results from the backend into a final form,
  or distributes to other workers for further processing.

The nice thing about using Celery in this model is that it does almost
all of the heavy lifting: to tackle an embarrassingly parallel
problem, you only need to install a broker and a backend and start the
workers running on all the computers you can get your hands on.

As an example, let's consider a classic Monte Carlo demonstration
problem: estimating :math:`pi`. Imagine a square with a side of length
1 inscribed with the first quadrant of the unit circle. If we throw
darts at the board, we can count how many land within the inscribed
circle and how many land outside. The area of the circle is given by

.. math::

   A = \frac{1}{4}\pi

This means that, assuming all darts hit the board, the probability of
a randomly thrown dart landing within the circle is the same as the
area. Therefore, we can estimate :math:`\pi` by throwing enough darts:

.. math::

  \pi \approx 4 \frac{M}{N}

where :math:`M` is the number of darts landing within the circle, and
:math:`N` the total number of darts thrown [#1]_. With a random number
generator, implementing a program to estimate :math:`\pi` in this
manner is straightforward [#2]_. For comparison, we should start with
the most naive approach possible, which is just using a for loop to
throw darts in sequence:

.. code-block:: python

   def try_point(point):
       """Throws a single dart and returns 1 if inside the target region,
       else 0.

       """
       x, y = point
       if x**2 + y**2 < 1:
           return 1.
       else:
           return 0.

   def process_results(inside, total):
       """Estimates pi given the number of darts that landed inside the
       target region and the total number of darts thrown.

       """
       if isinstance(inside, list):
           inside = np.sum(inside)
       return 4*inside/total

   def estimate_pi_naive(N):
       """Naively estimate pi."""
       print("Starting with naive single-threaded Python...")
       inside = 0
       for _ in range(N):
           inside += try_point(random((2,)))
       inside = np.sum(inside)
       print("pi is approximately", process_results(inside, N))

Now let's do this in parallel with celery. Because using celery
requires some network transport, we don't want to use a task that
throws just one dart, but instead have each celery worker throw
several darts [#3]_. The Python code defining the celery task is again
straightforward:

.. code-block:: python

   @app.task
   def try_points(N):
       """Throws N darts and returns the number that landed inside the
       target region. Separated from the celery task in order to work
       more easily with IPython's parallel model.

       """
       points = random((N, 2))
       inside = 0.
       for point in points:
           inside += try_point(point)
       return inside

Now to actually use this task, we have a function which submits a
series of of calls to :func:`try_points`:

.. code-block:: python

    def estimate_pi_celery(N_groups, N_per_group):
        """Estimate pi using celery. Monte Carlo tries are grouped in
        N_groups groups of size N_per_group.

        """
        print("Starting with celery...")
        res = chord(
            (try_points.s(N_per_group) for N in range(N_groups)),
            process_results.s(N_groups*N_per_group))()
        pi = res.get()
        print("pi is approximately", pi)

Here we are using a celery "chord," which is a way to add a callback
after several other tasks have completed. Now to start the celery
workers, we run the command:

.. code-block:: shell-session

   $ celery worker -A mcpi

Without any other options, this will spawn as many worker processes as
CPU cores on your machine. That's really all there is to it! In
principle, you can run more instances of celery on any computer and
they will listen for and process submitted tasks, making scaling
almost trivial.

.. _Numpy: http://www.numpy.org/
.. _embarrassingly parallel: https://en.wikipedia.org/wiki/Embarrassingly_parallel
.. _Monte Carlo simulations: https://en.wikipedia.org/wiki/Monte_Carlo_method
.. _IPython: http://ipython.org/
.. _Celery: http://www.celeryproject.org/

.. [#] For a more formal explanation, see here__.
.. [#] Full code for the examples is available on Github__.
.. [#] The exact balance of how you should group things is dependent
       on the problem. In practice, you would have to play around with
       the group size until you find a good number to use.

__ http://mathfaculty.fullerton.edu/mathews/n2003/montecarlopimod.html
__ https://gist.github.com/mivade/8e374f1a8e42a92a43ff
