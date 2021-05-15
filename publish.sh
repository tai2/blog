#!/bin/sh

pelican content -s publishconf.py
aws s3 cp --recursive output/ s3://tai2.net/blog/
