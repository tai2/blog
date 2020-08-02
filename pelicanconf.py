#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os import path

AUTHOR = 'tai2'
SITENAME = 'blog.tai2.net'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = 'ja'
IGNORE_FILES = ('*~', '*.swp')
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
FILENAME_METADATA = '(?P<slug>.*)'

THEME = 'blog.tai2.net-theme'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["simple_footnotes"]

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

def basename(str):
    return path.splitext(path.basename(str))[0]

JINJA_FILTERS = { 'basename': basename }
