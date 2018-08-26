# colorize-video
colorize video using neural-networks
### Referenced Code and Motivation
This code was inspired by the code that was written by Sunita Nayak at BigVision LLC. It is based on the OpenCV project.
I wanted to write a script (or a few) that would input a video and output a the video with original RGB removed and neural net generated colorization added.

Satya Mallick post that sparked interest:
* https://www.learnopencv.com/convolutional-neural-network-based-image-colorization-using-opencv/
## About colorize-video
* Input: Color or B&W Video File (preferably '*.mp4')
* Output: AI Colorized Video File
The neural network recreates each frame's colorization individually
### Youtube
Big Buck Bunny
30 second sample of colorization output video:
* https://youtu.be/I7DkwbDBRwI 
### Original
Original Big Buck Bunny Colorization

<div align="left">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/originalcolor-long-0-10.gif" />
</div>

### Colorized from Greyscale
Colorized Big Buck Bunny with Zero Knowledge of the Original Colorization

<div align="left">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/colorized-long-0-10-output.gif" />
</div>

### Greyscale
Greyscale Processed Frames

<div align="left">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/grey-long-0-10.gif" />
</div>

## Requirements
### FFmpeg
* FFmpeg command line tools
"A complete, cross-platform solution to record, convert and stream audio and video."
#### Linux (Ubuntu)
The simplest of all the land is our friend Ubuntu, where the following command would suffice for installation of ffmpeg library.
Make sure that ffmpeg is in your bin path etc if you are unable to enter in terminal after restart or after reinvoking bashrc using "source".
```shell
$ sudo apt-get install ffmpeg
```
#### Mac OS (Homebrew)
The simplest way to install ffmpeg on Mac OS X is with [Homebrew](http://mxcl.github.com/homebrew/).
Once you have Homebrew installed install ffmpeg from the Terminal with the following:
```
$ brew install ffmpeg
```
#### Windows
##### FFmpeg
Simplest way to get ffmpeg installed is to 
* https://www.ffmpeg.org/
* https://www.wikihow.com/Install-FFmpeg-on-Windows
extract the contents of the zip folder and add the directory containing only the extracted files to your PATH environment variables.
##### wget (Windows only necessary step)
running getModels.sh requires 'wget' which is not native to Windows 10
"A command-line utility for retrieving files using HTTP, HTTPS and FTP protocols."

I used version 1.19.4 which was found here:
https://eternallybored.org/misc/wget/
wget-1.19.4-win64.zip, wget.exe

extract the contents of the zip folder and add the directory containing only the extracted files to your PATH environment variables.
start a new Command Prompt and the wget command should be available
```shell
$ wget --version
```
After entering the -V --version command you should see something similar to the following command prompt output:
```shell
GNU Wget 1.19.4 built on mingw32.
... *a bunch of versioning text*...
    /win32dev/misc/wget/out64/lib/libiconv.a
    /win32dev/misc/wget/out64/lib/libunistring.a -lws2_32
...*a bunch of versioning text*...
Copyright (C) 2015 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later
... *a bunch of licensing text*...
```
Navigate back to the 'colorize-video/' directory and run
```shell
$ getModels.sh
```
### Python
I used Python 2.7.15 and 3.6.5
* https://www.python.org/downloads/
#### Packages
Using pip https://pypi.org/project/pip/
```shell
$ pip install numpy
$ pip install opencv-python
$ pip install imutils
```
* [NumPy](http://numpy.scipy.org/)
* [OpenCV 3](http://opencv.org/) 
* [Imutils](https://github.com/jrosebr1/imutils)
### Structure
```shell
*models/*  contains the models used in this example we use Facial Landmark detection 68 points.
```
```shell
*images/*  contains images 
*greyimages/*  contains grey scale images for colorization
*greyimages/coloredimages/*  contains colorized images 
```
### Installation
Open a terminal in the headpose directory and run (with sudo if needed on your system):
```shell
$ pip install -r requirements.txt
```
Now you should have installed the necessary packages

You still need to download the models: 
```python
#Specify the paths for the 2 model files
protoFile = "./models/colorization_deploy_v2.prototxt"
weightsFile = "./models/colorization_release_v2.caffemodel"
#weightsFile = "./models/colorization_release_v2_norebal.caffemodel"

# Load the cluster centers
./pts_in_hull.npy')
```
Give privilages to run the shell script to start application
```shell
$ chmod +x getModels.sh
$ chmod +x all_colorize.sh
$ chmod +x colorized_pngs2vid.sh
$ chmod +x pngs2vid.sh
```
Then run the shell script
```shell
$ ./getModels.sh
```
## Sample Video
### Original

<div align="center">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/originalcolor-short-15-3.gif" /><br><br>
</div>

### Colorized from Greyscale

<div align="center">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/colorized-short-15-3-output.gif" /><br><br>
</div>

### Greyscale

<div align="center">
<img src="https://github.com/mauckc/colorize-video/blob/master/sample-video/grey-short-15-3.gif" /><br><br>
</div>

## Usage
### Process input video and output all frames in greyscale
```shell
$ python grey-video2images.py
```
## Colorize all greyscale frames
```shell
$ ./all_colorize.sh
```
## Compile new video of colorized frames
```shell
$ ./colorized_pngs2vid.sh
```

The colorization part of this code is based on and adapted by the code that was written by Sunita Nayak at BigVision LLC. It is based on the OpenCV project.
It is subject to the license terms in the LICENSE file found in this distribution and at http://opencv.org/license.html

-Ross Mauck



