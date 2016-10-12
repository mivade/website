title: Simplifying argparse usage with subcommands
date: 2016-10-12
tags: python
---

One of the best things about Python is its standard library: it's
frequently possible to create complex applications while requiring few
(if any) external dependencies. For example, command line interfaces
can be easily built with the `argparse` module. Despite this, there
exist several alternative, third-party modules (e.g., [docopt][],
[click][], and [begins][]). These all tend to share similar
motivations: while `argparse` is powerful, it is by inherently verbose
and is therefore cumbersome to use for more complex CLIs which use
advanced features such as subcommands. Nevertheless, I tend to prefer
sticking with `argparse` in part because I am already familiar with
the API and because using it means I don't need to bring in another
dependency from PyPI just to add a small bit of extra
functionality. The good news is that with a simple decorator and a
convenience function, writing CLIs with subcommands in `argparse` is
pretty trivial and clean.

Start by creating a parser and subparsers in `cli.py`:

```py
from argparse import ArgumentParser

cli = ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")
```

Note that we are storing the name of the called subcommand so that we
can later print help if either no subcommand is given or if an
unrecognized one is. Now we can define a decorator to turn a function
into a subcommand:

```py
def subcommand(args=[], parent=subparsers):
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
	return decorator
```

What this does is take the wrapped function and use its name and
docstring for the subcommand name and help string, respectively. Next
it automatically adds arguments for the subcommand from a list passed
to the decorator. In order to dispatch the command later, the usual
`parser.set_defaults` method is used to store the function itself in
the `func` variable.

In the simplest case, we can create a subcommand which requires no
arguments as follows:

```py
@subcommand()
def nothing(args):
    print("Nothing special!")
```

Meanwhile, in our main function, we dispatch the subcommand as follows:

```py
if __name__ == "__main__":
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)
```

Now running `python cli.py nothing` will run the `nothing` function
and simply print `Nothing special!` to stdout.

More often, subcommands require their own set of options. In the
definition of the `subcommand` decorator above, these options can be
given as a list of length-2 lists that contain the [name or flags][]
for the argument and all keyword arguments used by
`ArgumentParser.add_argument`. This is a bit cumbersome as is, so it's
useful to define a small helper function that takes arguments just
like `ArgumentParser.add_argument`:

```py
def argument(*name_or_flags, **kwargs):
    return ([*name_or_flags], kwargs)
```

Now we can define commands with arguments like so:

```py
@subcommand([argument("-d", help="Debug mode", action="store_true")])
def test(args):
    print(args)


@subcommand([argument("-f", "--filename", help="A thing with a filename")])
def filename(args):
    print(args.filename)


@subcommand([argument("name", help="Name")])
def name(args):
    print(args.name)
```

That's all there is to it! Quite a bit better than [the default way][]
to build a CLI with subcommands. The full example can be found [here][].

[docopt]: http://docopt.org/
[click]: http://click.pocoo.org/
[begins]: http://begins.readthedocs.io/en/latest/
[name or flags]: https://docs.python.org/3/library/argparse.html#the-add-argument-method
[the default way]: https://docs.python.org/3/library/argparse.html#sub-commands
[here]: https://gist.github.com/mivade/384c2c41c3a29c637cb6c603d4197f9f
