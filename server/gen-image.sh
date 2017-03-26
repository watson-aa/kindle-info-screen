#!/bin/sh

cd "$(dirname "$0")"

python main.py
rsvg-convert --background-color=white -o tmp.png output.svg
pngcrush -c 0 tmp.png output.png
rm -f output.svg tmp.png
