#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os import path

AUTHOR = u'tai2'
SITENAME = u'blog.tai2.net'
SITEURL = ''

LOCALE = ('en_US', 'ja_JP')
TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = u'jp'
IGNORE_FILES = ('*~', '*.swp')
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
FILENAME_METADATA = '(?P<slug>.*)'

THEME = 'blog.tai2.net-theme'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_DATE = 'fs'
AUTHOR_SAVE_AS = ''

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["simple_footnotes"]

# Theme specific settings.
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_SUBMENU = False
DISPLAY_CATEGORIES_ON_POSTINFO = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

def basename(str):
    return path.splitext(path.basename(str))[0]

JINJA_FILTERS = { 'basename': basename }
