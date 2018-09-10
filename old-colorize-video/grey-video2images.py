#
# for dirs in di
import os
import cv2

# create directory for output images
directory = "greyimages/"

# if the out image directory does not already exist
if not os.path.exists(directory):
    # Create new directory
    os.makedirs(directory)

# create cv2 videoCapture instance
vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
# start capturing frames as image and return success
success,image = vidcap.read()
# start ascending image count
count = 0
# loop until VideoCapture returns false
while success:
  # Process frames
  grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
  # write to the frame (save frame as JPEG file) enumerated with count
  cv2.imwrite(directory+"/frame%04d.jpg" % count, grey)
  #read new image
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  # Iterate our image count
  count += 1
