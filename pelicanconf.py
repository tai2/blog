#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'tai2'
SITENAME = u'blog.tai2.net'
SITEURL = ''
AUTHOR_SAVE_AS = False

LOCALE = ('en_US', 'ja_JP')
TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = u'jp'
IGNORE_FILES = ('*~', '*.swp')
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

TYPOGRIFY = True
DISQUS_SITENAME = 'tai2'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/__tai2__'),
          ('facebook', 'https://www.facebook.com/taiju.muto'),
          ('github', 'https://github.com/tai2/'),)

DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
