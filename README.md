

<!-- toc -->

- [BillySTAT](#billystat)
  * [School project @Haaga-Helia University of Applied Sciences](#school-project-haaga-helia-university-of-applied-sciences)
    + [Project members](#project-members)
    + [Things to do](#things-to-do)
  * [Information page](#information-page)
  * [Setting up environment for YOLOv3](#setting-up-environment-for-yolov3)
    + [Setting up server](#setting-up-server)
      - [Creating access point for remote work](#creating-access-point-for-remote-work)
  * [Installations](#installations)
    + [Nvidia drivers](#nvidia-drivers)
    + [CUDA installation](#cuda-installation)
    + [OpenCV3](#opencv3)
    + [Installing Darknet](#installing-darknet)
    + [Installing Nextcloud for cloud-storage with docker-compose](#installing-nextcloud-for-cloud-storage-with-docker-compose)
    + [Nextcloud client for easy syncing](#nextcloud-client-for-easy-syncing)
  * [Training your neural networks](#training-your-neural-networks)
    + [Creating training material](#creating-training-material)
      - [Resizing images](#resizing-images)
      - [1st Alternative: YOLO-Annotation-Tool](#1st-alternative-yolo-annotation-tool)
      - [2nd Alternative: Open Labeling](#2nd-alternative-open-labeling)
      - [3rd Alternative: Yolo_mark by AlexeyAB](#3rd-alternative-yolo_mark-by-alexeyab)
  * [Actual training](#actual-training)
      - [Marking the images](#marking-the-images)
  * [Testing frame difference from video](#testing-frame-difference-from-video)
    + [Virtualenv](#virtualenv)
    + [Frame diff from video with grayscale](#frame-diff-from-video-with-grayscale)
    + [Frame diff with color](#frame-diff-with-color)
    + [Getting more material](#getting-more-material)
  * [Working with /matias](#working-with-matias)
    + [/bookmarks](#bookmarks)
    + [/custom](#custom)
    + [/swissair](#swissair)
    + [/snowman](#snowman)
    + [/snooker](#snooker)
  * [OpenCV Object selection by color, cv2.HoughCircles](#opencv-object-selection-by-color-cv2houghcircles)
    + [Defining ROIs](#defining-rois)
    + [Clear game area without Snooker-balls using GIMP and G'MIC](#clear-game-area-without-snooker-balls-using-gimp-and-gmic)

<!-- tocstop -->

# BillySTAT
BillySTAT records your Snooker statistics using YOLOv3, OpenCV and NVidia Cuda.

* [Darknet](https://pjreddie.com/darknet/install/)
* [YOLOv3](https://pjreddie.com/darknet/yolo/)
* [OpenCV3](https://www.learnopencv.com/install-opencv3-on-ubuntu/)

## School project @Haaga-Helia University of Applied Sciences
### Project members

- [Kristian Syrjänen](https://kristiansyrjanen.com/) 
- [Axel Rusanen](https://axelrusanen.com)
- [Miikka Valtonen](https://miikkavaltonen.com) **Project Manager**
- [Matias Richterich](https://matiasrichterich.com)

***Done on Xubuntu 18.04 LTS***

***Hardware HP z820, Xeon e52630 v2 x2, 2 x 8gb 1333 mHz per per processor, 1 TB SSHD***

***[Images of our setup](https://imgur.com/a/qfKz9Dd)***

### Things to do
***PRIO 1***
+ ~~Train new YOLOv3 weight!~~
+ Make OpenCV detection work!
+ ~~Setup server~~
+ ~~Install CUDA, OpenCV3, Darknet and YOLOv3~~
+ ~~Run basic tests~~
+ Make it recognise only things relevant (Done W/ YOLO)
+ Create boundaries that when crossed, counts as a point/points depending what colored ball it is.
+ Make it count statistics
+ Create GUI for statistics
+ ~~Gather image material~~

## Information page

[Thoughts, Ideas and Problems](https://github.com/kristiansyrjanen/billystat/blob/master/INFO.md)

## Setting up environment for YOLOv3
***(Laptop users attention: Getting your discrete gpu to work will be a driver-nightmare)***

### Setting up server
#### Creating access point for remote work

Config changes on 01-network-manager-all.yaml

    network:
    ethernets:
       enp1s0:
         addresses: [192.168.1.2/24]
         gateway4: 192.168.1.1
         nameservers:
           addresses: [1.1.1.1,8.8.8.8]
         dhcp4: no
     version: 2

And on our router we enabled port-forwarding to a desired port.

## Installations
### Nvidia drivers
First off we'll download NVidia drivers, let's start by adding nvidia ppa:latest,

    sudo add-apt-repository ppa:graphics-drivers
    sudo apt-get update

Install Nvidia drivers, (NOTE! At the time of writing, Cuda 10 FORCES 410 drivers. Meaning, if you have 415 or newer drivers installed, they will be uninstalled and replaced with 410 drivers. With some work this can be avoided, but you can just reinstall the newer drivers afterwards if necessary.)

    sudo apt-get install nvidia-driver-410

And reboot

    sudo reboot
    
### CUDA installation

Head on to the [download page](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=debnetwork), download the needed file and proceed with instructions.

    sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install cuda

We had trouble with apt-get so we used **aptitude**.

    sudo apt-get install aptitude
    sudo aptitude install cuda

Reboot and try out nvidia-smi

    nvidia-smi

### OpenCV3
This is taken from the OpenCV3 installation page.

**Install OS libraries**

    sudo apt-get update
    sudo apt-get upgrade

    sudo apt-get remove x264 libx264-dev

    sudo apt-get install build-essential checkinstall cmake pkg-config yasm
    sudo apt-get install git gfortran
    sudo apt-get install libjpeg8-dev libjasper-dev libpng12-dev
    
    sudo apt-get install libtiff5-dev
    
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
    sudo apt-get install libxine2-dev libv4l-dev
    sudo apt-get install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
    sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev
    sudo apt-get install libatlas-base-dev
    sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
    sudo apt-get install libvorbis-dev libxvidcore-dev
    sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
    sudo apt-get install x264 v4l-utils
    
    sudo apt-get install libprotobuf-dev protobuf-compiler
    sudo apt-get install libgoogle-glog-dev libgflags-dev
    sudo apt-get install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen
    
    sudo apt-get install python-dev python-pip python3-dev python3-pip
    sudo -H pip2 install -U pip numpy
    sudo -H pip3 install -U pip numpy
    
**Install Python libraries**

    sudo pip2 install virtualenv virtualenvwrapper
    sudo pip3 install virtualenv virtualenvwrapper
    echo "# Virtual Environment Wrapper"  >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    source ~/.bashrc
    
[//]: # (Python3)

    mkvirtualenv facecourse-py3 -p python3
    workon facecourse-py3
    
    pip install numpy scipy matplotlib scikit-image scikit-learn ipython
    // Exit virtual environment with deactivate
    deactivate
    
**Download opencv from Github**

    git clone https://github.com/opencv/opencv.git
    cd opencv 
    git checkout 3.3.1 
    cd ..
    
**Download opencv_contrib from Github**

    git clone https://github.com/opencv/opencv_contrib.git
    cd opencv_contrib
    git checkout 3.3.1
    cd ..
    
**Compile and install OpenCV with contrib modules**
**Create a build directory**

    cd opencv
    mkdir build
    cd build
    
**Run CMake**
    
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D WITH_GSTREAMER=ON \
      -D WITH_CUDA=ON \
      -D WITH_NVCUVID=ON \
      -D ENABLE_FAST_MATH=1 \
      -D CUDA_FAST_MATH=1 \
      -D WITH_CUBLAS=ON \
      -D CUDA_NVCC_FLAGS="-D_FORCE_INLINES" \
      -D BUILD_opencv_cudacodec=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=OFF ..
      
**Compile and Install**

    # find out number of CPU cores in your machine
    nproc
    # substitute 4 by output of nproc
    make -j 24
    sudo make install
    sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
    sudo ldconfig
    
**Create symlink in virtual environment**

    find /usr/local/lib/ -type f -name "cv2*.so"
    
    cd ~/.virtualenvs/facecourse-py3/lib/python3.6/site-packages
    ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
    
**Test it with C++**

    # compile
    # There are backticks ( ` ) around pkg-config command not single quotes
    g++ -std=c++11 removeRedEyes.cpp `pkg-config --libs --cflags opencv` -o removeRedEyes
    # run
    ./removeRedEyes
    
    workon facecourse-py3
    
**Test with Python3**

    python removeRedEyes.py
    // Exit virtual environment with deactivate
    deactivate

### Installing Darknet

	git clone https://github.com/pjreddie/darknet.git
	cd darknet
	make
	# No errors? Continue with running ./darknet

	./darknet
	# Output should look like:
	# usage: ./darknet <function>

Edit the Makefile in the base directory to get Darknet to use your CUDA/GPU:

	GPU=1

Also change the 2nd line of the Makefile:

	OPENCV=1
	# Try it with:
	# ./darknet imtest data/eagle.jpg

### Installing Nextcloud for cloud-storage with docker-compose

We decided to use docker-compose to create a container that runs Nextcloud so that we could easily share our training material (pictures/video). 

	cd
	mkdir nextcloud
	nano nextcloud/docker-compose.yml

We need a docker-compose.yml that looks like this,

	version: '3'

	volumes:
	  nextcloud:
	  db:

	services:
	  db:
	    image: mariadb
	    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
	    restart: always
	    volumes:
	      - db:/var/lib/mysql
	    environment:
	      - MYSQL_ROOT_PASSWORD=password
	      - MYSQL_PASSWORD=password
	      - MYSQL_DATABASE=nextcloud
	      - MYSQL_USER=username

	  app:
	    image: nextcloud
	    ports:
	      - 8080:80
	    links:
	      - db
	    volumes:
	      - nextcloud:/var/www/html
	    restart: always

Then just run docker-compose,

	sudo docker-compose up -d
	
Now we have Nextcloud running on our project-machine.

### Nextcloud client for easy syncing

To get our material easily synced between our machines we got ourselves the [Nextcloud client](https://nextcloud.com/install/#install-clients). We downloaded the Linux AppImage, changed permissions and ran it.

	chmod +x Nextcloud-2.5.1-x86_64.AppImage
	./Nextcloud-2.5.1-x86_64.AppImage

We added our Nextcloud path which to sync with.

	192.0.1.2:5050 #This is just an example-address and port-numbers
	
This way we all have the same material at all times and synchronized.

## Training your neural networks

### Creating training material

#### Resizing images

To resize the images to a smaller size we made a script that does it for us, let's call it *resize.sh*:

	FOLDER="/path/to/images"

	WIDTH=800

	HEIGHT=600

	find ${FOLDER} -iname '*.jpg' -exec convert \{} -verbose -resize $WIDTHx$HEIGHT\> \{} \;

Run it,

	./resize.sh # Or bash resize.sh, make sure you have x-rights correct
#### 1st Alternative: YOLO-Annotation-Tool

We went to a Pool & Snooker Bar called Corona and got some footage for our project.

Next we used [YOLO-Annotation-Tool](https://github.com/ManivanananMurugavel/YOLO-Annotation-Tool) to create training sets for YOLO.

	git clone https://github.com/ManivannanMurugavel/YOLO-Annotation-Tool.git
	
	cd YOLO-Annotation-Tool

Move our images to the 001 directory under ./YOLO-Annotation-Tool/Images .

	mv ./SnookerData/*.jpeg ./YOLO-Annotation-Tool/Images/001/

We need to remove the cat photos that are in the 001 directory which are all .jpg files.

	cd ./YOLO-Annotation-Tool/Images/001
	rm *.jpg

Next convert our .JPEG files to .JPG files

	mogrify -format jpg *.jpeg

To be able to run main.py we needed a few packages from apt.

	sudo apt-get install python-tk python-pil python-imaging-tk
	sudo pip install Image

Now we should be able to run main.py

	python main.py

The Labeling-Tool looks like this:

![Alt Text](https://i.imgur.com/19maPfz.gif) 

Although the labeling works well, we wouldn't get the program to run convert.py or process.py succesfully.
It would either create empty files or say that we didn't have some obscure directories (e.g. a directory with the name of our image).


#### 2nd Alternative: Open Labeling

We also tried another labeling-tool called [Open Labeling](https://github.com/Cartucho/OpenLabeling).

	git clone https://github.com/Cartucho/OpenLabeling.git

You can install everything at once by simply running:

	python -mpip install -U pip
	python -mpip install -U -r requirements.txt

Ran the program, shut it down and tried reopening it again and was greeted by Error messages. That was the first and last time we got it to work.

#### 3rd Alternative: Yolo_mark by AlexeyAB

Luckily we found an Annotation Tool called [Yolo_mark](https://github.com/AlexeyAB/Yolo_mark)  by the creator of Darknet, AlexeyAB.

First off:

	git clone https://github.com/AlexeyAB/Yolo_mark.git
	cd Yolo_mark

To compile it we ran 3 commands:

	cmake .
	make
	bash linux_mark.sh # Ctrl + C Ends

Set the number of classes (objects) in /x64/Release/yolo-obj.cfg on line 230.
Set filter value in /x64/Release/yolo-obj.cfg on line 224.

* for YoloV3 (classes + 5)*3

Now run Yolo_mark again and start making your BBoxes.

![Alt Text](https://i.imgur.com/O1JsSZs.gif)

## Actual training
***Please note: at the time of writing, this section is still a work in progress. Things may change and put simply, be completely wrong. We are still working out the best settings to yield the best results.***

***Also make sure have your labeling tool ready. We recommend Yolo_mark, it seems to be the best one out there by far.***

Let's start by copying and editing our config file:

         cp darknet/cfg/yolov3.cfg ../yolo-obj.cfg

Edit the line **batch** to **batch=64**.

Edit the line **subdivisions** to **subdivisions=64**. If your GPU has lots of memory (over 4GB), you can lower the subdivision number to 32, 16 or even 8.

Edit the line number 610 **classes** to whatever the amount of objects you want to detect is. For example, if you have 10 colors you have 10 classes.

Do the same for lines 696 and 783 as well.

Edit the line number 603 **filters** to whatever your amount of objects + 5 and multiply it by 3. (Objects+5)x3. For example, with 10 objects/classes, the correct filter number would be 45.

Do the same for lines 689 and 776 as well.

After this, create file **obj.names** in your darknet directory.

Write the names of all your objects you want to detect, each in their own line.

For example, if we wanted to detect colors, we would start listing: 1. Green, 2. Blue, 3. Yellow, and so on. **Make sure each object is in its own line!**

Next, create file **obj.data**. In it, fill the following information:

         classes= 10 //the number of your objects
         train = train.txt //you can change these paths if your directory structure differs
         valid = train.txt //^
         names = obj.names
         backup = backup/ //this is where backups of weights files are made, every 1000 lines I thin

#### Marking the images

Now comes the boring part. Make sure you have all your teaching material (.jpgs) ready in Yolo_mark/x64/Release/data/img/.

Back up a bit and launch Yolomark in its top directory:

	$ sh linux_mark.sh

![](https://i.imgur.com/Nvoa8j4.jpg)

It's time to start creating boxes. It's long and tedious work, but it needs to be done. You can change the Object ID from the lower slider, the upper slider can be used to browse pictures. Alternatively you can click the next picture from the top of the screen.

When you are done, you should have a text file for each respective .jpg file in Yolo_mark/x64/Release/data/img/. If this is correct, give yourself a tap on the back. 

Copy **obj.data**, **obj.names** and **train.txt** to your main darknet folder. (Or wherever you want, make sure you remember it.)

Now, open **train.txt**, and make sure it contains the location of every image. One image per line. Yolo_mark should create the file, but if you want to change the image location, you can do it here.

Great! Now before we can try training, we still need to download the premade training weights from the official site:

	$ wget http://pjreddie.com/media/files/darknet53.conv.74

And now, if you're feeling confident, we can finally attempt training:

	$ ./darknet detector train obj.data yolo-obj.cfg darknet53.conv.74

If all goes well, you should start seeing lots of numbers:

![Alt Text](https://i.imgur.com/k3sXNi0.gif)

Is text flashing before your eyes? Great! Do you see lots of -nan? Maybe not great, who knows at this point. This is what we are trying to find out. At the moment of writing, we  believe that some nans are tolerable, but you should start seeing less and less the longer you iterate.

If you run into CUDA memory errors, try editing the **yolo-obj.cfg** file. Worst case scenario, edit subdivions and batch to 64. You can also try editing the image dimensions, however keep in mind that they **must** be divisible by 32. Make a note of the original value in case you need to revert changes.

On an Nvidia GPU, you can open Nvidia X Server Settings to monitor GPU processor usage, as well as memory usage. It seems to be normal for the GPU usage % to jump around when training with Tiny cfg.

Darknet will generate a weights file every 100 iterations until it reaches 1000 iterations, after which a backup will be saved after every 1000 iterations.


## Testing frame difference from video

### Virtualenv

Either use earlier facecourse-py3 virtualenv or create a new one with suiting name.

We created a new one, *billystat*, the same way as the facecourse virtualenv.

	mkvirtualenv billystat -p python3
	workon billystat
	
	pip install numpy scipy matplotlib scikit-image scikit-learn ipython
	deactivate

Create symlink
	
	cd ~/.virtualenvs/billystat/lib/python3.6/site-packages
	ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so

### Frame diff from video with grayscale

	workon billystat
	
	python3 billyFRAME.py
	
![Alt Text](https://i.imgur.com/QO2VE2P.gif)

### Frame diff with color

We changed 

	current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
	previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
	
To

	current_frame_color = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
	previous_frame_color = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2RGB)

Which results in

![Alt Text](https://i.imgur.com/uYViSDV.gif)

This is nice but need something a bit different.

### Getting more material

So we headed out to [Tapanilan Urheilukeskus](https://tapanilanurheilu.fi/), who let us use their Snooker-tables and space, to film better material for our project. We used a good few hours and racked up about 1300 images and 2½ hours of footage. A special thanks goes to [Tapanilan Urheilukeskus](https://tapanilanurheilu.fi/).

## Working with /matias 

### /bookmarks

I've collected good sources and written some of about most useful articles. 

### /custom

This was first attempt to train YOLOv3 weights, not successful.

### /swissair

This was second attempt to train YOLOv3 weights. This time it started to iterate throught files, but without results. Something went wrong during training.

### /snowman

This was third attempt to train YOLOv3 weights. This time also program started to successfully iterate throught files. But because it was really doing something during training, it was so slow, it took about 20 hours to do 2000 iterations with my laptop. And that is why this one also "failed".

### /snooker

At the same time as I tried to work with snowman-detection, we build a completely working YOLOv3 configuration, which ended up with a working weight (which is not perfect). 

[YoloV3 with custom weights(Imgur)](https://i.imgur.com/bIW2KPW.gif)


## OpenCV Object selection by color, cv2.HoughCircles

We started with Adrian Rosebrock's ball tracking code which can be found from [here](https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)

Adrian's code drew a line on the largest green object in the picture, which was a useful starting point, but it is much easier than our actual problem.

We began by setupping OpenCV read from a video and then selecting pixels based on color and seperating these into contours.
It is okay detecting regions but the problem is defining the colors narrowly enough to avoid the false positives. This becomes especially problematic as most pool tables are not evenly lit. It also requires one or more consecutive ranges of colors, which means that cutting out stuff in the middle of the region is annoying.

Then we tried to use HoughCircles, which is an algorithm that tries to detect circles by edges extracted from a greyscale image.
[cv2.HoughCircles (Imgur)](https://i.imgur.com/qSMCdpg.gif)

Here the problem was also the balance between false positive and false negatives. Since the perspective makes the balls appear different sizes. It is hard to tell to the algorithm exactly what size sphere it is looking for and it will start to find circles from irrelevant background details.
[cv2.HoughCircles Problems (Imgur)](https://i.imgur.com/ib5b7su.jpg)

<a href="https://i.imgur.com/ib5b7su"><img src="https://i.imgur.com/ib5b7su.jpg" title="source: imgur.com" /></a>

As a result in order to resolve the problem we think that you would need to do several passes of selection by color and then using circle detection this could get you the location of the balls by color in the image assuming you can fine tune the selection criteria well enough. Also only selecting only the play area from the image helps, but it would be likely if the camera or the lightning changes that the parameteres would need to be tuned again. There are also interesting problems with artefacts like reflections on the balls by bright lights, which show up as white circles in the circle detection and white color in the color definition.

### Defining ROIs

We defined the region of interest as the pool table itself. It looks like a trapezoid thanks to the perspective, so the square ROI that is as default in OpenCV leaves alot of extra room at the sides. Thus we defined a simple function where you can set the edge points of a polygon with mouse clicks. Then we filled it as a convex polygon and masked the image with it. This results in a image that is black except for the play area.
[Example ROI (Imgur)](https://i.imgur.com/7y4xwGF.png)

<a href="https://i.imgur.com/7y4xwGF"><img src="https://i.imgur.com/7y4xwGF.png" title="source: imgur.com" /></a>

Currently we are thinking of the posibilities to merge OpenCV and YOLO.


### Clear game area without Snooker-balls using GIMP and G'MIC

Software used: [GIMP](https://www.gimp.org/downloads/) and [G'MIC](https://gmic.eu/download.shtml)

We forgot to take a photo of the snooker-table without balls so we need to clear out the playing field using GIMP. First of all we need a bunch of photos with ballls in different spots so that we can use G'MIC to get the median of the layers.

This ends up only removing the red balls as the rest of the balls are on their respective default places.

<a href="https://imgur.com/8liXoGK"><img src="https://i.imgur.com/8liXoGK.png" title="source: imgur.com" /></a>

Now we clear the rest of the balls using the cloning-tool and the smudge-tool to even out the green-color.

<a href="https://imgur.com/RCXXVyk"><img src="https://i.imgur.com/RCXXVyk.png" title="source: imgur.com" /></a>

### 2D Perspective warping

We either needed to get better material (from straight up-top) or to warp the perspective of our videos.

***Spoiler: We went a filmed new material but before that we tried out how it would turn out***

To warp the perspective of our material we need to use OpenCV's cv2.getPerspectiveTransform and cv2.warpPerspective function.

For this we need to pinpoint 4 coordinates of our image/video from where it should warp the perspective from, and 4 coordinates to which size it should warp it to.

You can definately see that the perspective is warped, as you look at the pockets they seem really odd looking.

<a href="https://i.imgur.com/g0KDgda.jpg"><img src="https://i.imgur.com/g0KDgda.jpg" title="source: imgur.com" /></a>


## Creating a GUI for BillySTAT

### Tkinter

Tkinter is a GuiProgramming toolkit for python and according to the Python wiki, it is also the [most commonly used](https://wiki.python.org/moin/TkInter).
There are many others but we decided to use it as we had heard of it before during our course.

### Mockup

A good way to visualize what you want for your GUI is to create a mockup, here's our version we'd like to create.

<a href="https://i.imgur.com/mvjoInD.jpg"><img src="https://i.imgur.com/mvjoInD.jpg" title="source: imgur.com" /></a>

### Creating the GUI

We'd never done anything related to python nor any GUI-developing so all of this is new to us. So naturally we need to read tkinter wiki's and do a bunch of tutorials to get a hang of it.

Resources used:

https://www.youtube.com/watch?v=RJB1Ek2Ko_Y

https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/

https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

https://www.hackanons.com/2018/08/python-3-project-gui-text-editor-using.html

https://docs.python.org/2/library/tkinter.html

http://effbot.org/tkinterbook/place.htm

After testing numerus different ways of creating the GUI we finally made something that resembles our mockup GUI.

<a href="https://i.imgur.com/OSKTQa6.png"><img src="https://i.imgur.com/OSKTQa6.png" title="source: imgur.com" /></a>

![Gif of the GUI](https://giant.gfycat.com/WelcomeBlackAmericanbobtail.webm)

At this point we still need to attach all of the functionalities to the GUI. At the moment all of the filedialog prompts are done.
