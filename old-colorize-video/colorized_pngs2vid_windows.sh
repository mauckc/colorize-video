ffmpeg -r 25 -i greyimages/coloredimages/frame%04d_colorized.jpg -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4
