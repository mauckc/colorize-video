#!/bin/bash
# colorize all photos in a folder
# first argument to this shell script is the filetype you wish to convert
for filename in greyimages/*.jpg; do
    echo "$filename"
    python TIMING_colorize.py --input "$filename"

done
