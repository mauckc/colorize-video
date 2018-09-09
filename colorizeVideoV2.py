# import the necessary packages
from __future__ import print_function
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os.path

# create directory for output images
# these will only be populated with images if you uncomment
originaldirectory = "images/originalimages/"
graydirectory = "images/grayimages/"
colorizedirectory = "images/colorizeimages/"
balcolorizedirectory = "images/balcolorizeimages/"

# if the out image directory does not already exist
if not os.path.exists(originaldirectory):
    # Create new directory
    os.makedirs(originaldirectory)

# if the out image directory does not already exist
if not os.path.exists(graydirectory):
    # Create new directory
    os.makedirs(graydirectory)

# if the out image directory does not already exist
if not os.path.exists(colorizedirectory):
    # Create new directory
    os.makedirs(colorizedirectory)

# if the out image directory does not already exist
if not os.path.exists(balcolorizedirectory):
    # Create new directory
    os.makedirs(balcolorizedirectory)

# Start timing
start = time.time()
print("\nStarting timing... \n")
# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser(description='Colorize A Video and Save four frames')
ap.add_argument("-i","--input",required=True),
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-f", "--fps", type=int, default=30,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="XVID",
	help="codec of output video")
# Default= MJPG for ".mp4" changed to "XVID" for ".avi" which is more robust
args = ap.parse_args()

if args.input==None:
    print('Please give the input grayscale image name.')
    print('Usage example: python3 write_to_video_colorize.py --input path/to/RGB input video --output path/to/name of output file.avi')
    exit()

if os.path.isfile(args.input)==0:
    print('Input file does not exist')
    exit()

# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")
fvs = FileVideoStream(args.input).start()
time.sleep(1.0)

fps = FPS().start()

#Specify the paths for the 2 model files
protoFile = "./models/colorization_deploy_v2.prototxt"
weightsFile = "./models/colorization_release_v2.caffemodel"
balweightsFile = "./models/colorization_release_v2_norebal.caffemodel"

# Load the cluster centers
pts_in_hull = np.load('./pts_in_hull.npy')

# Read the network into Memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
balnet = cv2.dnn.readNetFromCaffe(protoFile, balweightsFile)
# populate cluster centers as 1x1 convolution kernel
pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)

### TWEAK HYPER-PARAMETERS HERE?
net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

balnet.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
balnet.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

#from opencv2 sample
W_in = 224
H_in = 224

# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*args.codec)
writer = None
(h, w) = (None, None)
zeros = None
counter = 0

# loop over frames from the video file stream
while fvs.more():
	counter +=1
	print("\nGrabbing Frame: {}".format(counter))
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale (while still retaining 3
	# channels)
	frame = fvs.read()
	### FRAME PROCESSING GOES BELOW
	frame = imutils.resize(frame, width=450)
	grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayframe = np.dstack([grayframe, grayframe, grayframe])

	# check if the writer is None
	if writer is None:
		# store the image dimensions, initialzie the video writer,
		# and construct the zeros array
		(h, w) = frame.shape[:2]
		writer = cv2.VideoWriter(args.output, fourcc, args.fps,
			(w * 2, h * 2), True)
		zeros = np.zeros((h, w), dtype="uint8")
		end = time.time()

    ### FRAME PROCESSING GOES ABOVE
	img_rgb = (grayframe[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
	img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
	img_l = img_lab[:,:,0] # pull out L channel

	# resize lightness channel to network input size
	img_l_rs = cv2.resize(img_l, (W_in, H_in)) #
	img_l_rs -= 50 # subtract 50 for mean-centering

	balimg_rgb = (grayframe[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
	balimg_lab = cv2.cvtColor(balimg_rgb, cv2.COLOR_RGB2Lab)
	balimg_l = balimg_lab[:,:,0] # pull out L channel

	# resize lightness channel to network input size
	balimg_l_rs = cv2.resize(balimg_l, (W_in, H_in)) #
	balimg_l_rs -= 50 # subtract 50 for mean-centering


	net.setInput(cv2.dnn.blobFromImage(img_l_rs))
	ab_dec = net.forward()[0,:,:,:].transpose((1,2,0)) # this is our result

	(H_orig,W_orig) = img_rgb.shape[:2] # original image size
	ab_dec_us = cv2.resize(ab_dec, (W_orig, H_orig))
	img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
	img_bgr_out = np.clip(cv2.cvtColor(img_lab_out, cv2.COLOR_Lab2BGR), 0, 1)


	balnet.setInput(cv2.dnn.blobFromImage(balimg_l_rs))
	balab_dec = balnet.forward()[0,:,:,:].transpose((1,2,0)) # this is our result

	(H_orig,W_orig) = balimg_rgb.shape[:2] # original image size
	balab_dec_us = cv2.resize(balab_dec, (W_orig, H_orig))
	balimg_lab_out = np.concatenate((balimg_l[:,:,np.newaxis],balab_dec_us),axis=2) # concatenate with original image L
	balimg_bgr_out = np.clip(cv2.cvtColor(balimg_lab_out, cv2.COLOR_Lab2BGR), 0, 1)

    # Uncomment below to output individual jpgs for each frame to file structure
	# file structure:
	#  "colorize-video/images/" +
	#      "colorize-video/colorizeimages/" +
	#      "colorize-video/balcolorizeimages/" +
	#      "colorize-video/grayimages/" +
	#      "colorize-video/originalimages/" +
	'''#colorizeoutputFile = args.input[:-4]+'_colorized.jpg'
	colorizeoutputFile = '../colorizeimages/'args.input[:-4]+'_colorized.jpg'
	print(colorizeoutputFile)
	#time.sleep(0.01)
	cv2.imwrite(colorizeoutputFile, img_bgr_out*255)
	print('\nColorized image saved as '+colorizeoutputFile)

	#colorizeoutputFile = args.input[:-4]+'_colorized.jpg'
	balcolorizeoutputFile = '../balcolorizeimages/'args.input[:-4]+'_balcolorized.jpg'
	print(balcolorizeoutputFile)
	#time.sleep(0.01)
	cv2.imwrite(balcolorizeoutputFile, balimg_bgr_out*255)
	print('\nColorized image saved as '+balcolorizeoutputFile)

	grayoutputFile = '../grayimages/'args.input[:-4]+'_gray.jpg'
	print(grayoutputFile)
	#time.sleep(0.01)
	cv2.imwrite(grayoutputFile, gray)
	print('\gray image saved as '+grayoutputFile)

	originaloutputFile = '../grayimages/'args.input[:-4]+'_original.jpg'
	print(originaloutputFile)
	#time.sleep(0.01)
	cv2.imwrite(originaloutputFile, gray)
	print('\original image saved as '+originaloutputFile)'''
	# Set end time
	print("Ending Timing...\n")
	endlast = end
	end = time.time()
	last_time_elapsed = end - endlast
	time_elapsed = end - start
	print("\n[INFO] Total Program Execution Time Elapsed: {} \n[INFO] Time Since Last Frame: {}".format(time_elapsed,last_time_elapsed))
	# construct the final output frame, storing the original frame
	# at the top-left, the grayscale channel in the top-right, the colorized
	# channel in the bottom-right, and the atuo balanced colorized channel in the
	# bottom-left
	output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
	output[0:h, 0:w] = frame
	output[0:h, w:w * 2] = grayframe
	output[h:h * 2, w:w * 2] = img_bgr_out*255
	output[h:h * 2, 0:w] = balimg_bgr_out*255
	### FRAME POST-PROCESSING GOES BELOW
	# display the size of the queue on the frame
	#cv2.putText(output, "Queue Size: {}".format(fvs.Q.qsize()),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
	# write the output frame to file
	writer.write(output)

	# show the frames
	#cv2.imshow("Frame", frame)
	cv2.imshow("Output", output)
	key = cv2.waitKey(1) & 0xFF

	# show the frame and update the FPS counter
	#cv2.imshow("Frame", frame)
	cv2.waitKey(1)
	fps.update()

print("\ndone!!!")
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
fvs.stop()
writer.release()
