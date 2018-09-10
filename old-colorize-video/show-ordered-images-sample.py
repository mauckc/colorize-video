# list comprehensions sample
from __future__ import print_function
import glob
import cv2
import time

from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
'''
https://stackoverflow.com/questions/38675389/python-opencv-how-to-load-all-images-from-folder-in-alphabetical-order
Luckily, python lists have a built-in sort function that can sort strings using ASCII values. It is as simple as putting this before your loop:
'''
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output",type=str,default="output.mp4", required=False,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=0,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
args = vars(ap.parse_args())

filenames = glob.glob("greyimages/*.jpg")
filenames.sort()
images = [cv2.imread(img) for img in filenames]
print(len(images))
time.sleep(0.5S)

# initialize the FourCC, video writer, dimensions of the image, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = None
(h, w) = (None, None)
zeros = None

for img in images:
    #print img
    cv2.imshow('image',img)
    time.sleep(0.05)
	# grab the image from the video stream and resize it to have a
	# maximum width of 300 pixelsa
	#img = imutils.resize(img, width=300)
	# check if the writer is None
    if writer is None:
        # store the image dimensions, initialzie the video writer,
		# and construct the zeros array
		(h, w) = img.shape[:2]
		writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
			(w, h), True)
		zeros = np.zeros((h, w), dtype="uint8")

    output = img
    # write the output image to file
    writer.write(output)

    key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
		break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
#vidcap.stop()
writer.release()
