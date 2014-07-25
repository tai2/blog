#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'tai2'
SITENAME = u'blog.tai2.net'
SITEURL = ''

LOCALE = ('en_US', 'ja_JP')
TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = u'jp'
IGNORE_FILES = ('*~', '*.swp')
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
FILENAME_METADATA = '(?P<slug>.*)'

THEME = 'built-texts-custom'
TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

SOCIAL = (('twitter', 'https://twitter.com/__tai2__'),
          ('facebook', 'https://www.facebook.com/taiju.muto'),
          ('github', 'https://github.com/tai2/'))

LINKS = (('tai2.net', 'http://tai2.net/'),
         ('blog.mikiishijima.com', 'http://blog.mikiishijima.com/'),
         ('Article Candidates', 'https://gist.github.com/tai2/5cb13126ed4ebb79a73d'))

DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'
AUTHOR_SAVE_AS = False

PLUGIN_PATH = "plugins"
PLUGINS = ["simple_footnotes"]

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
