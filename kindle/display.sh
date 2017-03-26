#!/bin/sh

cd "$(dirname "$0")"

rm output.png
eips -c
eips -c
if -O output.png wget http://server/path/to/output.png; then
	eips -g output.png
else
	eips -g error.png
fi
