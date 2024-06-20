---
title: Custom backends for cachetools
date: 2024-06-20
draft: true
tags:
  - python
  - caching
---

[cachetools][] is a popular library for Python that provides a number of caching tools. In addition
to providing decorators to easily memoize function and method calls it provides implementations for
several common cache invalidation algorithms. While the cache decorators can take an arbitrary
`MutableMapping` as the cache backend, the cache classes currently only work with an in-memory
dictionary stored as a name-mangled `__data` attribute. Although there is [an
issue](https://github.com/tkem/cachetools/issues/232) logged for this, the maintainer doesn't seem
to be interested in changing this. Of course it is always fine for an open source maintainer to
choose which issues to address and which to leave as is but I often want to be able to use a cache
backed by something other than an in-memory dict.

Luckily there is an easy workaround by consulting the Python documentation on [private name
mangling](https://docs.python.org/3/reference/expressions.html#atom-identifiers). Here is a simple
example:

```python
from cachetools import Cache


class MyBackend(dict):
    def __repr__(self):
        return "hi there, I'm a custom backend"


class MyCache(Cache):
    def __init__(self):
        super().__init__(maxsize=10)
        self._Cache__data = MyBackend()


cache = MyCache()
cache["foo"] = "foo"
cache["bar"] = "bar"
print(cache["foo"])
print(cache["bar"])
print(cache)
```

Running this script results in the following output:

```
foo
bar
MyCache(hi there, I'm a custom backend, maxsize=10, currsize=2)
```



[cachetools]: https://pypi.org/project/cachetools/
