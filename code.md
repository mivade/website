Code
====

See also my repositories on [GitHub][].

[GitHub]: https://github.com/mivade

Web stuff
---------

* [mdscript.py][] - A script that utilizes Markdown to make fully
  XHTML compliant html files. I formerly used this to create all of my
  web pages, since editing plaintext files is a lot easier to read and
  maintain than HTML files. I then used [Sphinx][] for a while
  instead, but switched back to Markdown using [Python Markdown][].
* [genfeed.py][] - A script to generate an atom feed from a directory
  containing text files.

[mdscript.py]: old/mdscript.html
[Sphinx]: http://sphinx-doc.org/
[Python Markdown]: http://pythonhosted.org/Markdown/
[genfeed.py]: code/genfeed.py

Physics/Math
------------

* [mcpi][] - A "Monte Carlo" method of calculating pi (I was bored).
* [optbloch][] - Evaluates the optical Bloch equations for a two level
  system using simple time step integration.
* [wigner.py][] - Python module for evaluating Clebsch-Gordan
  coefficients and Wigner 3- and 6-j symbols. 9-j symbols are not yet
  implemented. (Note: This has *not* been thoroughly tested, but all
  values that I have checked have given correct results).

[mcpi]: /code/mcpi.cpp
[optbloch]: /code/optbloch.cpp
[wigner.py]: /code/wigner.py

Miscellaneous
-------------

* [arxivsum.py][] - Aggregates [arXiv][] RSS feeds and sends you an
  email with new abstracts from the categories you want. This is meant
  to be something you can run daily as a cron job. The only required
  non-standard module is [feedparser][] which is available in
  [Debian][]'s apt repository.
* [cfbrank][] - A (so far overly simplistic) ranking of US college
  football teams.

[arxivsum.py]: /code/arxivsum.py
[arXiv]: http://www.arxiv.org
[feedparser]: http://www.feedparser.org/
[Debian]: http://www.debian.org
[cfbrank]: https://github.com/mivade/cfbrank
