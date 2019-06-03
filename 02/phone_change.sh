#!/usr/bin/env bash

DIRECTORY=${1:-"/var/www"}
find $DIRECTORY -type f -iname '*.htm' -iname '*.html' ?
