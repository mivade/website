#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Michael V. DePalatis'
SITENAME = u'mike.depalatis.net'
SITEURL = 'http://mike.depalatis.net'
PATH = 'content'

THEME = 'themes/mvd'
THEME_STATIC_DIR = 'theme'
THEME_STATIC_PATHS = ['theme', 'static']

# pelican-bootstrap3 theme options
BOOTSTRAP_THEME = 'flatly'
BOOTSTRAP_NAVBAR_INVERSE = False
PYGMENTS_STYLE = 'native'
HIDE_SIDEBAR = True

TIMEZONE = 'Europe/Copenhagen'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_LANG = u'en'

MD_EXTENSIONS = [
    'codehilite(css_class=highlight)',
    'extra',
    'footnotes'
]

DEFAULT_CATEGORY = "Blog"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS = ()

# Social widget
#SOCIAL = (('github', 'https://github.com/mivade'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DEBUG = True

