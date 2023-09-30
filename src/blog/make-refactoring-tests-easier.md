---
title: Make refactoring tests easier
date: 2023-09-30
tags:
  - python
  - testing
---

Quite often when I see unit tests written by colleagues I'll see this sort of
pattern:

```python
from package.subpackage.blah import foo, bar, baz
```

On the surface there doesn't seem to be anything wrong with this. But what
happens when you decide that `foo` doesn't really belong in `subpackage` let
alone `blah` and that it instead should live in `package.other_subpackage`? A
good IDE like [PyCharm](https://www.jetbrains.com/pycharm/),
[VS Code](https://code.visualstudio.com/), or a properly configured
[Emacs](https://www.gnu.org/software/emacs/) provides you with helpful
refactoring tools that will adjust your imports to read something like

```python
from package.subpackage.blah import bar, baz
from package.other_subpackage.fizz import foo
```

This is a good start but to keep things properly organized you'll likely need
to manually move the unit test code to an appropriately named module, too. When
I write unit tests if I have a package structure like

```
package
|__ __init__.py
|__ subpackage
    |__ __init__.py
    |__ blah.py
|__ other_subpackage
    |__ __init__.py
    |__ fizz.py
```

I like to lay out my test modules with a one-to-one correspondence with the
package's module:

```
test_package
|__ __init__.py
|__ test_subpackage
    |__ __init__.py
    |__ test_blah.py
|__ test_other_subpackage
    |__ __init__.py
    |__ test_fizz.py
```

So in this case I want to move my tests for `foo` into `test_fizz.py`. For a
single test case this is not a big deal, but with more things being moved around
it can get tricky. One thing I've found that makes it exceedingly easy to move
code around is in unit tests import the module under test as `module`:

```python
from package.subpackage import blah as module
```

Now all your tests will refer to `foo` as `module.foo` so when you move those
around to somewhere else all you need to do is have a similar import statement
at the top of your test module.

This may seem like a small thing but I've found it quite helpful. Another useful
feature of importing the module instead of each part individually is that as
your modules grow you don't need to have giant import statements: everything is
already there under the `module` namespace.
