# colorize-video
colorize video using neural nets

## About colorize-video

---
### Referenced Code
* https://www.learnopencv.com/convolutional-neural-network-based-image-colorization-using-opencv/
* https://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/

### Requirements
You need to have Python 2.6+ as a minimum and:

* [NumPy](http://numpy.scipy.org/)
* [OpenCV 3](http://opencv.org/) 
* [Imutils](https://github.com/jrosebr1/imutils)

### Structure
```shell
*python/*  the code.
```
```shell
*models/*  contains the models used in this example we use Facial Landmark detection 68 points.
           *one must download shape_detector_68_facial_landmarks.dat because it is too large a file to host here.
```
```shell
*images/*  contains images 
*greyimages/*  contains grey scale images for colorization
*greyimages/coloredimages/*  contains colorized images 
```
### Installation

Open a terminal in the headpose directory and run (with sudo if needed on your system):
```shell
pip install -r requirements.txt
```
Now you should have installed the necessary packages

You still need to download the models: 

```python
Specify the paths for the 2 model files
protoFile = "./models/colorization_deploy_v2.prototxt"
weightsFile = "./models/colorization_release_v2.caffemodel"
#weightsFile = "./models/colorization_release_v2_norebal.caffemodel"

# Load the cluster centers
./pts_in_hull.npy')
```
	
Give privilages to run the shell script to start application

```shell
chmod +x getModels.sh
chmod +x all_colorize.sh
chmod +x colorized_pngs2vid.sh
chmod +x pngs2vid.sh
```

Then run the shell script
```shell
	./getModels.sh
```

## Usage
### Process input video and output all frames in greyscale
```shell
python grey-video2images.py
```
## Colorize all greyscale frames
```shell
./all_colorize.sh
```

## Compile new video of colorized frames
```shell
./colorized_pngs2vid.sh
```

 This code has been adapted by the code tbat was written by Sunita Nayak at BigVision LLC. It is based on the OpenCV project.
 It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

---
-Ross Mauck



