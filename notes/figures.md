Scientific Figures
==================

This page contains a collection of notes on ways I've found to make
good publication quality figures using a variety of open source
tools. I've gone back and forth between several different plotting
tools, but have now settled on [Matplotlib][].

[Matplotlib]: http://matplotlib.org/

General Considerations
----------------------

Figures should be sized to match the width of the text. This is
particularly important in two column formats, though I sometimes find
with single columns, having a figure a little bit smaller than the
text width can look nicer. To get a pleasing looking figure, the
height should be the an integer times the width divided by the
[golden ratio][].

The font face and size should match the text of the document. For
journals using standard LaTeX fonts, this is generally pretty easy,
though exactly how to do this depends on what tool is being used (see
notes below for specifics).

[golden ratio]: http://en.wikipedia.org/wiki/Golden_ratio

Matplotlib
----------

I have developed a lot of this from following [1][] as well as several
other sources that I don't recall now.

Getting figures sized correctly with Matplotlib used to be a huge
pain. More recent versions have simplified things significantly,
though it still is not as easy as it should be. This is because figure
size and margins have to be set separately. In versions past, this was
a pretty tedious process of trial and error until it looked good
enough. Now you can use the [tight_layout][] function to adjust the
margins (mostly) automatically for you.

In principle, you can write common settings to the `matplotlibrc`
file. However, since things like figure sizes, font faces, font sizes,
etc. may change depending on your target, I find the best way to deal
with things is have a simple template file which contains all commonly
used settings.

[tight_layout]: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.tight_layout

Gnuplot
-------

[Gnuplot][] used to be my primary plotting tool. Several reasons why I
no longer use it for publication quality output:

1. Although it's possible to do some simple data processing with it,
   anything more complex really requires doing it externally and
   saving to an intermediate data file from which Gnuplot can do it's
   thing.
2. The output terminals will all produce different results. The easy
   way to get around this is pick an output format to always use and
   convert to whatever else you need later.
3. There is an annoying bug that I found involving misalignment of
   tick labels (I believe in the `epslatex` terminal, but I'm not
   completely sure now). I filed a bug report with a workaround, but
   the bug report was closed. The workaround was too annoying for me
   to want to deal with it. If I can find the details on what I had to
   do, I'll post it here later.

I should note that Gnuplot is still a great tool, and there are plenty
of reasons you might still want to use it:

1. It's really easy for making quick plots.
2. Output quality can be very good without too much work.
3. A lot of its plot commands have really natural syntax that is easy
   to remember.
4. Its nonlinear least squares fitting routine works really well and
   is very easy to use.

To summarize: Gnuplot has its issues (but so does everything else). If
you're willing to deal with its slight quirks, it can be an excellent
tool.

Some helpful links:

* [Gnuplot demos][]: This is pretty exhaustive if you need to figure
  out how to do something.
* [Gnuplot not so Frequently Asked Questions][gpnfaq]

[Gnuplot]: http://gnuplot.info/
[Gnuplot demos]: http://gnuplot.info/screenshots/index.html#demos
[gpnfaq]: http://security.riit.tsinghua.edu.cn/~bhyang/ref/gnuplot/index-e.html

Inkscape
--------

[Inkscape][] is a wonderful vector graphics editor. It can be useful
for making 2-D diagrams, sophisticated illustrations, or annotating
plots. I prefer TikZ (see below) for a lot of my drawings, but it's
not always suitable.

[Inkscape]: http://inkscape.org/

TikZ
----

Lots of examples [here][texample].

Scaling is pretty easy with TikZ, since font sizes stay the same and
only the drawing portion is scaled with the scale option of the
`tikzpicture` environment. Often the diagrams I make with TikZ are
combined with other figures externally with Inkscape, so scaling to
the text width is not generally necessary. However, when it is,
[this][tikz scaling] method works well.

[texample]: http://www.texample.net/tikz/
[tikz scaling]: http://tex.stackexchange.com/a/6391

### References ###

[1]: http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
