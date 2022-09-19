---
title: Using ART with Wayland
date: 2022-09-19
tags: linux, photography, art, rawtherapee, photo-editing
---

Lately I've been experimenting with using
[ART](https://bitbucket.org/agriggio/art/wiki/Home), a raw photo editing
application which is a fork of [RawTherapee](http://rawtherapee.com/). Compared
to the excellent [Darktable](https://www.darktable.org/), ART has a slightly
easier learning curve and can yield decent results pretty quickly. The binaries
provided for Linux however do not work on
[Wayland](https://en.wikipedia.org/wiki/Wayland_(display_server_protocol)) and
the official recommendation is to build binaries yourself. Luckily there is a
much easier workaround by setting the `GDK_BACKEND` environment variable:

```
GDK_BACKEND=x11 ./ART
```