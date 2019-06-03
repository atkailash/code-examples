#!/usr/bin/env bash

DIRECTORY=${1:-"/var/www"}
echo $DIRECTORY
echo "find $DIRECTORY -type f -iname '*.html' -name '*.htm' -print0"
find $DIRECTORY -type f -regex ".*\.\(htm\(l\)?\)" -print0 | xargs -0 sed -r -i -f ./sed.txt
