#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Michael V. DePalatis'
SITENAME = u'mike.depalatis.net'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Copenhagen'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_LANG = u'en'

MD_EXTENSIONS = [
    'codehilite(css_class=highlight)',
    'extra'
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS = ()

# Social widget
#SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
