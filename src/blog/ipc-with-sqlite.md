---
title: Sharing data between processes with SQLite
date: 2017-03-19
tags: sqlite, python, multiprocessing
---

Because of the global interpreter lock in CPython, it is sometimes beneficial to
use separate processes to handle different tasks. This can pose a challenge for
sharing data: it's generally best to avoid sharing memory between processes for
reasons of safety[^1]. One common approach is to use pipes, queues, or sockets
to communicate data from one process to another. This approach works quite well,
but it can be a bit cumbersome to get right when there are more than two
processes involved and you just need to share a small amount of infrequently
changing data (say some configuration settings that are loaded after worker
processes have already been spawned). In such cases, using a file that each
process can read is a simple solution, but may have problems if reading and
writing happen simultaneously. Thankfully, [SQLite][] can handle this situation
easily!

I have created a small module ([Permadict][]) which utilizes SQLite to persist
arbitrary (picklable) Python objects to a SQLite database using a dict-like
interface. This is not
a
[new](https://pypi.python.org/pypi/sqldict/0.5.2) [idea](https://dataset.readthedocs.io/en/latest/),
but it was fun and simple to utilize only the Python standard library to
accomplish this. A basic usage example:

```python
>>> from permadict import Permadict
>>> d = Permadict("db.sqlite")
>>> d["key"] = "value"
>>> print(d["key"])
value
```

Because context managers are great, you can also use permadicts that way:

```python
>>> with Permadict("db.sqlite") as d:
...     d["something"] = 1.2345
...
>>> with Permadict("db.sqlite") as d:
...     print(d["something"])
...
1.2345
```

[^1]: Of course, Python allows you to share memory among processes by using a
    [manager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing-managers),
    but this is not always possible depending on the specific use case.

[SQLite]: https://sqlite.org/
[Permadict]: https://pypi.python.org/pypi/permadict
