# avconv -r 10 -i image%04d.jpg -b:v 1000k test.mp4
ffmpeg -framerate 25 -pattern_type glob -i 'greyimages/*.jpg' -vcodec rawvideo -pix_fmt yuv420p grey-big-buck-bunny_720p_5mb.mp4
