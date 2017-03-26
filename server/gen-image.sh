#!/bin/sh

cd "$(dirname "$0")"

python main.py
rsvg-convert --background-color=white -o output.png output.svg
pngcrush -c 0 -ow output.png
