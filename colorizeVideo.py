# This code is written by Sunita Nayak at BigVision LLC. It is based on the OpenCV project.
# It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html
''''
(29 minutes) / 738 images at 1280x720 =
2.38683128 seconds
25 per minute
'''
#### Usage example: python3 colorize.py --input greyscaleImage.png
import numpy as np
import cv2
import argparse
import os.path
import time
import os
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Colorize GreyScale VideoStream')
ap.add_argument('-i','--input', required=True,help='Path to Video.')
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-f", "--fps", type=int, default=25,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default='MPG4',
	help="codec of output video")
args = ap.parse_args()
argnovars = vars(ap.parse_args())

if args.input==None:
    print('Please give the input greyscale video name.')
    print('Usage example: python3 colorizeVideo.py --input greyscaleVideo.mp4 --output colorizedVideo.mp4')
    exit()

if args.output==None:
    print('Please give the output colorized video name.')
    print('Usage example: python3 colorizeVideo.py --input greyscaleVideo.mp4 --output colorizedVideo.mp4')
    exit()

if os.path.isfile(args.input)==0:
    print('Input file does not exist')
    exit()


# create directory for output images
directory = "greyimages/"

# if the out image directory does not already exist
if not os.path.exists(directory):
    # Create new directory
    os.makedirs(directory)

# create directory for output images
directory = "greyimages/coloredimages/"

# if the out image directory does not already exist
if not os.path.exists(directory):
    # Create new directory
    os.makedirs(directory)

# create cv2 videoCapture instance
vidcap = cv2.VideoCapture(args.input)

# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*argnovars["codec"])
writer = None
(h, w) = (None, None)
zeros = None

# start capturing frames as image and return success
success,image = vidcap.read()
# start ascending image count
count = 0
# loop until VideoCapture returns false


# Specify the paths for the 2 model files
protoFile = "./models/colorization_deploy_v2.prototxt"
weightsFile = "./models/colorization_release_v2.caffemodel"
#weightsFile = "./models/colorization_release_v2_norebal.caffemodel"

# Load the cluster centers
pts_in_hull = np.load('./pts_in_hull.npy')

# Read the network into Memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# populate cluster centers as 1x1 convolution kernel
pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

#from opencv sample
W_in = 224
H_in = 224

while success:
    # Start timing
    start = time.time()
    print("\nStarting timing... \n")
    # Process frames
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
    # write to the frame (save frame as JPEG file) enumerated with count
    cv2.imwrite(directory+"/frame%04d.jpg" % count, grey)
    #read new image
    success, image = vidcap.read()
    print('Read a new frame: ', success, count)
    if writer is None:
      # store the image dimensions, initialzie the video writer,
      # and construct the zeros array
      (h, w) = image.shape[:2]
      print( image.shape[:2] )
      #writer = cv2.VideoWriter(args.output, fourcc, args.fps,
      #(w * 2, h * 2), True)
      writer = cv2.VideoWriter(argnovars["output"], fourcc, argnovars["fps"], (w, h), True)
      zeros = np.zeros((h, w), dtype="uint8")
	# Read the input image
    frame = image

    img_rgb = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
    img_l = img_lab[:,:,0] # pull out L channel

    # resize lightness channel to network input size
    img_l_rs = cv2.resize(img_l, (W_in, H_in)) #
    img_l_rs -= 50 # subtract 50 for mean-centering

    net.setInput(cv2.dnn.blobFromImage(img_l_rs))
    ab_dec = net.forward()[0,:,:,:].transpose((1,2,0)) # this is our result

    (H_orig,W_orig) = img_rgb.shape[:2] # original image size
    ab_dec_us = cv2.resize(ab_dec, (W_orig, H_orig))
    img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
    img_bgr_out = np.clip(cv2.cvtColor(img_lab_out, cv2.COLOR_Lab2BGR), 0, 1)
    # check if the writer is None
    #print(img_bgr_out*255)
    #output = img_bgr_out*255
    writer.write(cv2.resize(img_bgr_out*255,(h, w)))
    # Set end time
    print("Ending Timing...\n")
    end = time.time()
    time_elapsed = end - start
    print("\nTotal Program Execution Time Elapsed: {} ".format(time_elapsed))

    # Iterate our image count
    count += 1
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
  	    break
print("\ndone!!!")
# Do cleanup
print("[INFO] cleaning up...")
vidcap.stop()
writer.release()

'''
# start late options
count = 0
# loop until VideoCapture returns false
while success:
    if count > 1829:
      # Process frames
      grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
      # write to the frame (save frame as JPEG file) enumerated with count
      cv2.imwrite(directory+"/frame%04d.jpg" % count, grey)
      #read new image
      success,image = vidcap.read()
      print('Read a new frame: ', success)
      # Iterate our image count
      count += 1
	else:
	  count += 1
'''
