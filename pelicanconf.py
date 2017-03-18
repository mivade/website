#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Michael V. DePalatis'
SITENAME = u'mike.depalatis.net'
SITEURL = 'https://mike.depalatis.net'
PATH = 'content'
STATIC_PATHS = ["img", "notebooks"]
PAGE_PATHS = ["pages"]
OUTPUT_PATH = './output'

# Menu settings
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
# I shouldn't have to do this!!!
MENUITEMS = [("About", "about.html"), ("Resources", "resources.html")]

# Theme settings
THEME = 'themes/mvd'
THEME_STATIC_DIR = 'theme'
THEME_STATIC_PATHS = ['theme', 'static']
BOOTSTRAP_THEME = 'yeti'
BOOTSTRAP_NAVBAR_INVERSE = False
PYGMENTS_STYLE = 'default'
HIDE_SIDEBAR = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

# Date settings
TIMEZONE = 'US/Eastern'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_LANG = u'en'

# URL settings
ARTICLE_URL = "blog/{slug}.html"
ARTICLE_SAVE_AS = "blog/{slug}.html"
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"
SLUGIFY_SOURCE = "basename"

# Markdown extensions and options
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.footnotes": {}
    },
    "output_format": "html5"
}

# Blog settings
DEFAULT_CATEGORY = "Blog"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS = ()

# Social widget
#SOCIAL = (('github', 'https://github.com/mivade'),)

DEFAULT_PAGINATION = 5

SUMMARY_MAX_LENGTH = 250

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DEBUG = True
