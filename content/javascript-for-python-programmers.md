title: Javascript for Python programmers
date: 2016-09-21
status: draft
tags: python, javascript, web, programming

Unless you're just writing a simple HTTP API server, any amount of web
programming in Python will likely require a little bit of
Javascript. Like it or not (and I will try to argue in this post that
you should like it for what it's good at), Javascript is really the
only game in town when it comes to client-side scripting on a web
page. Sure, there are a [number][1] of [Python-to-Javascript][2]
[transpilers][3] [out][4] [there][5], but using these just tends to
limit the ability to use new Javascript features as they are rolled
out to browsers and may limit the ability to use third-party
Javascript libraries, and at the very least, it introduces some bit of
added complexity to deploying a web app[^1].

In this post, I will describe some things I've learned about
Javascript from the perspective of someone who prefers to use Python
as much as possible. It is assumed that the reader is at least
moderately familiar with Javascript (Mozilla has [a nice tutorial][jstut]
to get you up to speed if not).

[1]: http://pyjs.org/
[2]: https://github.com/chrivers/pyjaco
[3]: https://github.com/anandology/pyjs
[4]: https://github.com/pypyjs/pypyjs
[5]: http://www.transcrypt.org/
[jstut]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript

## Namespaces, encapsulation, modularization, and bundling

Modules in Python make it very easy to encapsulate components without
polluting the global namespace. In contrast, Javascript in the browser
will make everything a global if you are not careful[^2]. The good
news is that it doesn't require too much extra effort to use a sort of
module pattern in your Javascript code thanks to things like object
literals and [closures][]. Imagine you are writing some code to do
some simple math operations that aren't in the Javascript
[`Math`][jsmath] library. Instead of doing this:

```javascript
// Don't do this
function mean(x) {
  var i;
  var total = 0;
  for (i = 0; i < x.length; i++) {
    total += x[i];
	}
  return total/x.length;
}
```

you should prefer putting your functions in an object:

```javascript
// This is better
var mathlib = {
  mean: function (x) {
    var i;
    var total = 0;
    for (i = 0; i < x.length; i++) {
      total += x[i];
	}
    return total/x.length;
  }
};
```

An even better approach is to wrap your definitions in a closure to
keep things better encapsulated:

```javascript
// This is even better!
var mathlib = (function (lib) {
  lib.mean = function (x) {
    var i;
    var total = 0;
    for (i = 0; i < x.length; i++) {
      total += x[i];
	}
    return total/x.length;
  };

  return lib;
})(mathlib || {});
```

This pattern allows for splitting various components in building a
larger module into different files if necessary (a good idea when
things get complex enough to justify it). Rather than go into further
details, I'll refer you to an excellent article on the
[module pattern in Javascript](http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html)
by Ben Cherry.

## Bundling

HTTP/1.1 requires a new connection for every requested Javascript
file. While this problem is rectified in HTTP/2, not many web servers
and hosting providers support it yet as of late 2016. This has led to
[many][browserify] [different][webpack] [options][rollup] for bundling
multiple Javascript files into one file which can be included in a web
page with a single `script` tag. While these tools can be highly
tempting to use, I highly recommend avoiding them in almost all cases
for the following reasons:

1. They require having [Node.js][] installed. If you've read this far,
   you can probably handle that, but if your scientist colleagues
   aren't as experienced as you are with software development, asking
   them to have two entirely different language runtimes installed
   just to run the latest version of your helpful web interface is
   asking a bit too much.
2. The churn in Javascriptland is too fast-paced for those of us who
   have other things to spend our time on (although from my outsider's
   perspective, things appear to be settling down a bit lately).
3. Bundling files makes Javascript debugging a bit more difficult
   insofar as it usually requires also building source maps. While
   most of the Javascript bundlers will do this for you if asked, it
   just adds to the overall complexity.
4. The module pattern presented above is already sufficient in many
   cases. After all, what's a few milliseconds to load a second
   Javascript file from a server on your LAN?

A good, (potentially) pure Python approach to bundling your Javascript
files (for cases where it makes to split code into more than a single
file) is the [webassets][] module. Webassets has a lot of available
filters to run Javascript and CSS files through some extra steps
(including possible transpilation from other languages), but the
basics of it are pretty simple. Here's a sample Tornado app:

```python
import tornado.web
import tornado.ioloop
from webassets import Environment


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, assets):
        self.assets = assets

    def get(self):
        self.render("index.html", assets=assets)


# Set up the webassets environment and make a bundle
assets = Environment(directory=".", url="/static")
js_files = ["mathlib.js", "thing.js", "class-example.js"]
assets.register("bundle", *js_files,
                output="bundled.min.js",
                filters="rjsmin")  # webassets always includes this filter

app = tornado.web.Application(
    [(r'/', MainHandler, dict(assets=assets))],
    static_path=".",
    template_path=".",
    debug=True)

app.listen(8123)
tornado.ioloop.IOLoop.current().start()
```

To include the bundled file in the template, you would do something
like this in the template:

```html
{% for url in assets['bundle'].urls() %}
  <script src="{{ url }}"></script>
{% end %}
```

The careful reader may wonder why the for loop is used if all the
Javascript files will be bundled into a single file in the end. This
is because webassets has a helpful debug mode to make debugging
Javascript in the browser easier. By adding ``assets.debug = True`` to
the Python file, ``assets['bundle'].urls()`` will return a list of all
the original, uncompressed Javascript file. This results in individual
script tags for each Javascript source file which is typically what
you want for debugging even if it does increase loading overhead a
little.

There are a lot of nice features in webassets, though many of the
filters require third-party tools (often using Node.js) to be
installed. For this reason, I discourage using most of these until and
unless you are comfortable with the rabbit hole of the Node world.

(**Aside**: Recently, I learned of the
[DukPy](https://github.com/amol-/dukpy) interpreter. While it's still
early, it looks like a promising way of being able to include things
that currently require Node-based tools while keeping everything
purely Pythonic.)

[closures]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures
[jsmath]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math
[browserify]: http://browserify.org/
[webpack]: https://webpack.github.io/
[rollup]: http://rollupjs.org
[Node.js]: https://nodejs.org/en/
[webassets]: https://webassets.readthedocs.io/en/latest/

## Embracing the present

Among Python programmers, Javascript has a tendency to be considered a
very poor programming language in terms of features and syntax. While
this was once a more valid criticism, Javascript has steadily
improved, and especially with the introduction of the [ES2015][]
standard, it's a very comfortable language to work in[^3]. In this
section, I will cover a few of the more useful features made available
in ES2015 with the small caveat that using them requires using fairly
up-to-date browsers (which is not normally a problem among scientists
who in my experience are all using either Firefox or Chrome, anyway).

### Arrow functions

In Python, `self` by convention refers to the instance of a
class. This means that even with nested function definitions, the
reference to `self` is always unambiguous, so you could do something
like

```python
class Thing:
    def __init__(self, value):
		self.value = value

    def method(self):
	    def function():
		    return self.value
		return function()
```

and expect calling the `method` method on an instance of `Thing` to
correctly return `thing.value`. In Javascript, the approximate
equivalent of `self` is `this` which is by default bound *as a
reference to the function being called*. In other words,

```javascript
var thing = {
  value: 1,
  method: function () {
    var func = function () {
      return this.value;
    };
    return func();
  }
};

console.log(thing.method());
```

will print `undefined` because `func` has no `value` attribute. This
can be fixed by explicitly binding `this` to `func` (`func =
func.bind(this)`), but this quickly becomes cumbersome when the number
of functions that need this fix grows. In part to simplify this,
ES2015 introduced so-called [arrow functions][] which are kind of like
Python lambdas on steroids. One nice feature of arrow functions is
that they lexically bind the `this` variable so we can rewrite the
above to read

```javascript
var thing = {
  value: 1,
  method: function () {
    var func = () => this.value;
    return func();
  }
};

console.log(thing.method());
```

which correctly outputs `1`.

### Classes

Prior to ES2015, classes in Javascript had to be implemented with a
function:

```javascript
function MyClass(value) {
  this.value = value;
}

var instance = new MyClass(10);
```

Implementing inheritance was cumbersome and required the use of the
`prototype` attribute:

```javascript
function Programmer(language) {
  this.language = language;
}

// Add a method to the Programmer prototype
Programmer.prototype.programThings = function () {
  console.log("Favorite language: " + this.language);
  console.log(this instanceof Programmer);
};

// Create child classes
function PythonProgrammer() {
  Programmer.call(this);
  this.language = "Python";
}

PythonProgrammer.prototype = Object.create(Programmer.prototype);

function JavascriptProgrammer() {
  Programmer.call(this);
  this.language = "Javascript";
}

JavascriptProgrammer.prototype = Object.create(Programmer.prototype);

var pythonProgrammer = new PythonProgrammer();
var jsProgrammer = new JavascriptProgrammer();

pythonProgrammer.programThings();
jsProgrammer.programThings();

/* Output:

Favorite language: Python
true
Favorite language: Javascript
true */
```

With ES2015, classes can be defined in a more Pythonic way:

```javascript
class MyBaseClass {
  constructor(value) {
    this.value = value;
  }

  method() {
    return this.value;
  }
}

class MyNewClass extends MyBaseClass {
  secondMethod() {
    return this.value + 1;
  }
}

var instance = new MyNewClass(10);
console.log(instance.method());
console.log(instance.secondMethod());
```

which outputs

```
10
11
```

### Template strings

Despite the [Zen of Python][] suggesting that "there should be one--
and preferably only one --obvious way to do it," there are 3 ways to
format strings as of Python 3.6. The newest of these ways is the
so-called "f-string" introduced by [PEP 498][]. This allows you to
have variables dynamically inserted into strings without having to
explicitly use %-formatting or the `str.format` method:

```python
x = 20
print(f'{x} is 20')
```

ES2015 has a similar concept in template strings:

```javascript
var x = 20;
console.log(`${x} is 20.`);
```

Like Python docstrings, Javascript template strings can also span
multiple lines:

```javascript
`this is
ok
even if it is
a pointless string.`
```

### Iterators, generators, and promises

One of the most useful features of Python is to be able to easily
iterate over a list:

```python
for x in y:
    print(x)
```

Javascript has long had, for example, `Array.prototype.forEach()` to
iterate over an array, but this requires the use of a callback
function to act on each value in the array. Javascript now has the
more Pythonic `for ... in` and `for ... of` statements:

```javascript
var list = [1, 2, 3, 4, 5];
var obj = {
  a: 1,
  b: 2,
  c: 3
};

// for ... in on list makes x take on the *indeces* of list
console.log("for (x in list)");
for (let x in list) {
  console.log(x);
}

// for ... of on list makes x take on the *values* of list
console.log("for (x of list)");
for (let x of list) {
  console.log(x);
}

// for ... in on obj makes x take on the *keys* of obj
console.log("for (x in obj)");
for (let x in obj) {
  console.log(x);
}
```

Generators are used frequently in Python to efficiently iterate over
values without having to pre-compute and store in memory each loop
iteration's result. In Javascript, a function must explicitly be
declared a generator by denoting it a `function*` and using the
familiar `yield` keyword:

```javascript
function* itsATrap() {
  while (true) {
    yield "What is it?";
    yield "It's a trap!";
  }
}

var isItATrap = itsATrap();
console.log(isItATrap.next().value);
console.log(isItATrap.next().value);
console.log(isItATrap.next().value);
console.log(isItATrap.next().value);
```

### Other newer features

There are quite a few other nice things introduced by ES2015, but the
above illustrates features that are perhaps the most welcomed by
Python programmers. For a good overview of all newer Javascript
features, see [this][babeles2015], for example.

[ES2015]: http://www.ecma-international.org/ecma-262/6.0/
[arrow functions]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
[Zen of Python]: https://www.python.org/dev/peps/pep-0020/
[PEP 498]: https://www.python.org/dev/peps/pep-0498/
[babeles2015]: https://babeljs.io/docs/learn-es2015/

## Frameworks

There is a ridiculous number of frontend Javascript frameworks
available. Luckily, as with tooling, things seem to be calming a bit,
with [React][] and a few others being the most popular. With the
exception of web apps that are updating more than a few elements (or
updating more frequently than every few minutes) to reflect changes in
conditions in real time, I would avoid any of these and instead stick
to built-in functions like `document.querySelector` to update elements
on a web page which is rendered with server-side templates as much as
possible. Not only are server-side templates easy to write and
understand, but they are often much faster to render on slow devices
such as ARM-based smartphones compared to client-side rendering
approaches of many Javascript frameworks.

However, there are plenty of times when you might want to write a
simple web interface to present real-time updates (e.g.,
[Brush][]). For these cases, I recommend [Vue][]. Vue takes a
template-based approach to updating views while having a simple and
easy-to-learn API that works well in the browser without requiring
transpiling (unlike React with JSX).

[React]: https://facebook.github.io/react/
[Brush]: https://brush.readthedocs.io/en/latest/
[Vue]: https://vuejs.org/

## Pythonic Javascript cheat sheet

To summarize, what follows are a series of short snippets showing some
common Pythonic concepts and their Javascript analogs.

### Exception handling

```python
try:
    thing()
except Exception:
    print("oh no!")

raise ValueError("not a good value")
```

```javascript
try {
  thing();
} catch (error) {
  console.error("oh no!");
}

throw "not a good value";
```

### Iterators

```python
arr = [1, 2, 3]
obj = {
    "a": 1,
    "b": 2,
    "c": 3
}

for val in arr:
    print(val)

for key in obj:
    print(key)
```

```javascript
var arr = [1, 2, 3];
var obj = {
  a: 1,
  b: 2,
  c: 3
};

for (let val of arr) {
  console.log(val);
}

// or...
arr.forEach((value, index) => {
  console.log(value);
});

for (let key in obj) {
  console.log(key);
}
```

### Generators

```python
def gen(x):
    while True:
        yield x
        x = x + 1
```

```javascript
function* gen(x) {
  while (true) {
    yield x;
    x++;
  }
}
```

### Classes

```python
class Thing:
    def __init__(self, a):
        self.a = a

    def add_one(self):
        return self.a + 1

class OtherThing(Thing):
    def __init__(self, a, b):
        super(OtherThing, self).__init__(a)
        self.b = b

    def add_things(self):
        return self.a + self.b
```

```javascript
class Thing {
  constructor(a) {
    this.a = a;
  }

  addOne() {
    return this.a + 1;
  }
}

class OtherThing extends Thing {
  constructor(a, b) {
    super(a);
    this.b = b;
  }

  addThings() {
    return this.a + this.b;
  }
}
```

### Functional programming

#### Lambdas

```python
expression = lambda a, b: a + b
```

```javascript
// Arrow functions are more powerful than Python lambdas, but not in
// this example!
let expression = (a, b) => a + b;

// or...
let sameThing = function (a, b) {
  return a + b;
}
```

#### MapReduce

```python
from functools import reduce

mapped = map(lambda a: a + 1, range(10))
print(reduce(lambda a, b: a + b, mapped))
```

```javascript
let arr = [];
for (let i = 0; i < 10; i++) {
  arr.push(i);
}
let mapped = arr.map((a) => a + 1);
console.log(arr.reduce((a, b) => a + b));
```

[^1]: Not that modern Javascript tooling is really so good at reducing
complexity... More on this later.

[^2]: Of course, there are tools like [webpack](https://webpack.github.io/)
that can let you use modern Javascript modules in the browser, but
this requires the step of bundling all the Javascript sources into
a browser-friendly bundle. Unless you are willing to dive deep into
the, um, interesting world of Javascript tooling, I recommend against
this as you get started with more complex Javascript.

[^3]: Although it would be a lot nicer if there were actually a
standard library to speak of.
