# avconv -r 10 -i image%04d.jpg -b:v 1000k test.mp4
ffmpeg -framerate 25 -pattern_type glob -i 'greyimages/coloredimages/*.jpg' colorized-big-buck-bunny_720p.mp4
