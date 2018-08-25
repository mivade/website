---
title: Getting Matplotlib's colors in order
date: 2016-07-21
tags: matplotlib, python
---

[Matplotlib][] can be very easy to use at times, especially if you
just want to make a simple "y vs. x" type of plot. But when it comes
to specialized customization, it can be a bit challenging to find the
proper solution. The situation is not helped by the fact that a lot of
times, an obscure answer on Stack Overflow no longer works because the
API changed.

One common need is to color things in the same way. For example, say
you want to plot two dependent variables with widely different scales
that share an independent variable. This is often represented by
having two separate vertical axes which are colored to match the lines
or markers of each data set. The most basic approach is to manually
assign colors for the lines and axes, but if using a custom [style][],
such as the `ggplot` style, we need a way to access the color cycle
used if we want to remain consistent with the selected style. Here is
the best way I have found which works at least in version 1.5:

```python
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
```

`colors` should now be a list which contains the colors defined in
order by the current style.

[Matplotlib]: http://matplotlib.org/
[style]: http://matplotlib.org/users/style_sheets.html
