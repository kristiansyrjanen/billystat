# BillySTAT
#### BillySTAT records your Snooker statistics using ~~YOLOv3~~, OpenCV ~~and NVidia Cuda~~.


<a href="https://i.imgur.com/hZDxVAB.png"><img src="https://i.imgur.com/hZDxVAB.png" title="HUD for BillySTAT" /></a>

<a href="https://i.imgur.com/fDvP2RI.png"><img src="https://i.imgur.com/fDvP2RI.png" title="GUI for BillySTAT" /></a>


**How to use BillySTAT:**

In folder billystat/kristian-kesken/gui/ run command


	python billystatApp.py

Choose video to analyse: File->Open and choose the video and press Start game

Next

Click outermost points of the snooker table on the displayed video for mask and press C. Then mark the pockets by clicking on them and press C again. It should start running.

Simple as that.

#### Our achievements in action @ https://www.youtube.com/channel/UCiSQy3Upsj8ocebaWwPHvFQ

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
  * [YOLOv3 Does not suit for detecting fast small objects](#yolov3-does-not-suit-for-detecting-fast-small-objects)
  * [Testing frame difference from video](#testing-frame-difference-from-video)
    + [Virtualenv](#virtualenv)
    + [Frame diff from video with grayscale](#frame-diff-from-video-with-grayscale)
    + [Frame diff with color](#frame-diff-with-color)
    + [Getting more material](#getting-more-material)
  * [OpenCV Object selection by color, cv2.HoughCircles](#opencv-object-selection-by-color-cv2houghcircles)
    + [Defining ROIs](#defining-rois)
    + [Empty game area without Snooker-balls using GIMP and G'MIC](#empty-game-area-without-snooker-balls-using-gimp-and-gmic)

<!-- tocstop -->

# BillySTAT
BillySTAT records your Snooker statistics using ~~YOLOv3~~, OpenCV ~~and NVidia Cuda~~.

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

***Done with***

* [Darknet](https://pjreddie.com/darknet/install/)
* [YOLOv3](https://pjreddie.com/darknet/yolo/)
* [OpenCV3](https://www.learnopencv.com/install-opencv3-on-ubuntu/)

***Hardware HP z820, Xeon e52630 v2 x2, 2 x 8gb 1333 mHz per per processor, 1 TB SSHD***

***[Images of our setup](https://imgur.com/a/qfKz9Dd)***

### Things to do
***PRIO 1***
+ ~~Train new YOLOv3 weight!~~
+ ~~Make OpenCV detection work!~~
+ ~~Setup server~~
+ ~~Install CUDA, OpenCV3, Darknet and YOLOv3~~
+ ~~Run basic tests~~
+ ~~Make it recognise only things relevant~~
+ Create boundaries that when crossed, counts as a point/points depending what colored ball it is.[Undertesting]
+ ~~Make it count statistics~~
+ ~~Create GUI for statistics~~
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


## YOLOv3 Does not suit for detecting fast small objects 

As part of our school course we are doing a project with Yolov3 and OpenCV. 
We are a group of 4 and two of us are working with YOLOv3 and rest are working with OpenCV. 
Our goal is to detect snooker balls from live video and count statistics, as potting percent from overall hits, from it. 
We started this project with about minimal coding experience with python and zero experience with artificial intelligence. 
We like to take the deep end from the pool, that is where you learn to swim.  

Matias and Miikka were working with YOLOv3. 
Westarted our experiment from basically setting up our computer environments for GPU based computing and testing different proof of concepts following PJReddie’s darknet, Adrian Rosebrock’s and Learnopencv.com’s tutorials. At the same time, we read a bunch of theory and got know what we are working with. As we haven’t worked with YOLOv3 or any artificial intelligence-based image recognition programs before, at the beginning every configuration file and whole concept was a complete mystery for us. 
But as we dug deeper, solved problems on the way and spent many hours with YOLOv3, we managed to get proper results. 
We managed to apply tutorials to our own needs, and we proceeded training our own YOLOv3 weights. 

Of course, before we started the training, we had to get everything we needed, so we went to Tapanilan Urheiluhalli to gather material for our own weight file. 
We recorded a couple hours of video of us playing snooker and couple thousand photos of the snooker balls themselves. 
Most of our video material was captured with a GoPro HERO5 BLACK. 
Some footage was also captured with a professional grade system camera. 
Pictures were all taken with the two system cameras we had. 
We opted to use a GoPro because of its good wide-angle lens. 
Its good resolution in addition to the large field of view meant that we would be able to capture the whole snooker table, and hopefully transform it into a 2D image. 
That would then allow us to process the images more easily. 
Later we found out however, that our setup was not optimal, as perhaps the distance between the table and the GoPro might have been too big, and YOLO was unable to do much with the footage because of the resulting unclearness in the video picture.
This however is purely guessing, as more testing should be done to be sure. 
We divided all photos for everyone from our team for annotating.
Annotating is a process where the user must mark the items of interest from the photo by dragging boxes over them and assigning a name for it. 
The item of interest “data” is then saved to a file, that can be shown to YOLO. 
This is how YOLO starts to identify objects from videos and photos, this is what we basically call training. 
During our tests we tried using multiple annotating programs and finally settled on Yolo_mark. 
Most of the programs were quite identical in their function, but user interfaces varied wildly. 
It was quite clear that most of them were written solely by and for their creators use and as such, worked barely enough for them to work. 
Out of all the programs tried, Yolo_mark was the only one that never crashed, did what it was supposed do and even the interface was bearable. 
Suffice to say, the ~1500 images that we processed in a few days should be taken as proof of it working.  

Configuring darknet to train custom weights is somewhat simple. For the first snooker ball detection weight we used tiny-yolo configuration, which proved to be relatively accurate and efficient. It took about 40 hours of computing to get 30k iterations. Our setup had Nvidia GTX 980 GPU and AMD Ryzen 5 1600 CPU. Your mileage may vary, depending the hardware used. Here are some samples to visualize our tiny-yolo weight performance.  

![alt text](https://i.imgur.com/R5qD0qi.png)

![alt text](https://i.imgur.com/qmUSVO3.gif)

![alt text](https://i.imgur.com/hoohCN2.gif)

After analyzing our work, we noticed that YOLO does detect balls that don’t move almost without a hitch. 
But as soon they start moving, it hardly recognizes them if at all. 
We started to investigate and go through our video footage more closely and soon concluded that even with the equipment we had, we were unable to capture footage at a high enough framerate for the balls to remain identifiable even when they move. 
With our current setup when you pause when a ball is moving it is a stretched, malformed, unidentifiable object, which only a human could recognize. 
We never set out to create a program that uses high performance computers and -cameras which record at hundreds of thousands of frames per second. 
Mainly because we don’t have budget for that, but also because we wanted to test and learn object detection programs available today and possibilities right now. 
Maybe if we had top notch equipment or simply more time, we would have had a different experience with YOLOv3 object detecting, but with these consumer grade cameras and deadlines, we didn’t get the results we expected.  

Before deciding to abandon YOLOv3 we gave it one more chance. 
There exist multiple pre-configurations for YOLOv3. 
Our previous weight file was based on the Tiny-yolo configuration, which is aimed towards low performance setups. 
As such training it was very much faster. 
This is how we were able to create our initial tests and verify that the training works. 
The second weight file we worked on was created with the proper Yolo configuration files. 
It is currently not exactly known to us how the proper Yolo configuration differs from tiny-yolo. 
We have noticed that the proper configuration file is at the very least three or even four times as long. 
One can only guess, that this means that the proper configuration file processes a lot more data in every cycle. 
Naturally this means that the training takes a lot longer too. 
As the tiny-yolo configuration and resulting weight file were quite successful we had high expectations of the proper, full configuration. 
As previously stated, it took around 40 hours to reach 30k iterations. 
Because of the huge time sink we were very hopeful that we are working with something special, but unfortunately it turned out to be a letdown. 

![alt text](https://i.imgur.com/xj4NXHg.gif)

It turned out that our previous tiny-yolo weights easily outperformed the proper 30k weights. 
We have read about the concept of “overtraining” an AI, where the AI learns the test images so well that it becomes unable to identify anything from new images. 
It is hard to say whether this has happened in our case, but that is what we would look at, had we more time. 
We are very interested in solving this issue, but unfortunately, we simply do not have the time to do so. 
As a result, we had no choice but to drop attempting to work with YOLOv3. 
We believe we can achieve the same things more effectively by building a simple program with OpenCV.
It is proving to be more suitable for detecting fast small objects and allows us to warp the processed image in various ways to ease our future steps, such as calculating and comparing ball and pocket coordinates. 
Next up on our list, is transforming a video image to a 2D image, from which we can hopefully gather and list coordinates.  


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

This is nice but we need something a bit different.

### Getting more material

So we headed out to [Tapanilan Urheilukeskus](https://tapanilanurheilu.fi/), who let us use their Snooker-tables and space, to film better material for our project. We used a good few hours and racked up about 1300 images and 2½ hours of footage. A special thanks goes to [Tapanilan Urheilukeskus](https://tapanilanurheilu.fi/).


## OpenCV Object selection by color, cv2.HoughCircles

We started with Adrian Rosebrock's ball tracking code which can be found from [here](https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)

Adrian's code drew a line on the largest green object in the picture, which was a useful starting point, but it is much easier than our actual problem.

We began by setting up OpenCV to read from a video and then selecting pixels based on color and seperating these into contours.
It is good in detecting regions but the problem is defining the colors narrowly enough to avoid the false positives. This becomes especially problematic as most pool tables are not evenly lit. It also requires one or more consecutive ranges of colors, which means that cutting out stuff in the middle of the region is annoying.

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

### Working on the Pallo.py

To separate the balls from the background and other objects we first removed everything that is colored like the table this leaves us with several contours which are balls, groups of balls, nets at the edges of the table and players. To figure which one of these are balls we fit a bounding ellipse on each area of sufficient size. Because there is aberration from the lens and perspective, we allow the area to deviate from perfect sphere somewhat, so all contours that are within a threshold of perfect ellipse are counted as balls. The downside of this that we don’t recognize group of balls as separate balls.

Once we have our balls, we calculate their center and their mean color in hsv-space. We then make a division between white ball and others. In order to track how successful the shot is we use simple logic. When the white ball has moved several frames, we consider that the shot has started, if other balls show consistent moving during the shot, we count it as successful, otherwise not. The shot ends when white ball has stayed still during several frames. This is necessary because areas are not completely still even if the object has not moved. Then we keep statistic of successful and unsuccessful hits and show them to the user from our terminal, but we are making a HUD for this.

<a href="https://i.imgur.com/3Uf9RY9.png"><img src="https://i.imgur.com/3Uf9RY9.png" title="source: imgur.com" /></a>

We can click the holes to mark them, if this is done, we will also attempt to see if any balls vanished near these locations. If they did then we count this as a ball going into the hole. We made some jerry-rigged contraption to catch some corner cases in calculating areas and ellipses because the nets are sometimes within the tolerance we have set, so they appear as balls vanishing and reappearing.

Currently our program crashes when there are no other balls left, we should try to figure something out for this problem, but its not critical at the moment. Also we aren't able to track the black ball as the default color for the mask is black, so we are trying to figure out a way to change the mask color to e.g. purple.


## Possible solutions to detecting balls from an angled view

We had problems detecting the balls from our table because of the angled view. The balls were being shadowed by other balls and the walls of the table, which had a huge impact in recognition. We scrambled through ideas that would help us get better results.

### Subtracting/Comparing frames

We thought about using an empty image of our snooker table to subtract from our live footage to leave only the relevant objects on the table. For this we needed an image of an empty snooker-table.

#### Empty game area without Snooker-balls using GIMP and G'MIC

Software used: [GIMP](https://www.gimp.org/downloads/) and [G'MIC](https://gmic.eu/download.shtml)

We forgot to take a photo of the snooker-table without balls so we needed to clear out the playing field using GIMP. First of all we need a bunch of photos with balls in different spots so that we can use G'MIC to get the median of the layers.

This ends up only removing the red balls as the rest of the balls are on their respective default places.

<a href="https://imgur.com/8liXoGK"><img src="https://i.imgur.com/8liXoGK.png" title="source: imgur.com" /></a>

Now we clear the rest of the balls using the cloning-tool and the smudge-tool to even out the green-color.

<a href="https://imgur.com/RCXXVyk"><img src="https://i.imgur.com/RCXXVyk.png" title="source: imgur.com" /></a>

### 2D Perspective warping

We either needed to get better material (from straight up-top) or to warp the perspective of our videos to read the game from a two dimensional point of view.

***Spoiler: We went a filmed new material but before that we tried out how it would turn out***

To warp the perspective of our material we need to use OpenCV's cv2.getPerspectiveTransform and cv2.warpPerspective function.

For this we need to pinpoint 4 coordinates of our image/video from where it should warp the perspective from, and 4 coordinates to which size it should warp it to.

You can definitely see that the perspective is warped, as you look at the pockets they seem really odd looking.

<a href="https://i.imgur.com/g0KDgda.jpg"><img src="https://i.imgur.com/g0KDgda.jpg" title="2D Perspective-warping" /></a>

### Solution to our recognition problem (Birdview footage)

The perspective warping result and the rest of our problems regarding the recognition of the snooker balls forced us to find a better angle to shoot our material from, which was the birdview. All of this was possible by lifting the tablelamps a meter higher than they usually were and strapping our Go Pro to a self-made camera-holder.

<a href="https://i.imgur.com/5unPZ51.jpg"><img src="https://i.imgur.com/5unPZ51.jpg" title="sMacGyver-apparatus" /></a>

This MacGyver-apparatus was made with a zigzag rule and 3 general-clamps, which totaled to cost 8,47€.

By filming from this angle and height we managed to get material in which we had full view of our snooker-table and no balls were being shadowed entirely by another ball or the walls.

## Creating a GUI for BillySTAT

### Tkinter

Tkinter is a GuiProgramming toolkit for python and according to the Python wiki, it is also the [most commonly used](https://wiki.python.org/moin/TkInter).
There are many others but we decided to use it as we had heard of it before during our course.

### Mockup

A good way to visualize what you want for your GUI is to create a mockup, here's our version we'd like to create.

<a href="https://i.imgur.com/mvjoInD.jpg"><img src="https://i.imgur.com/mvjoInD.jpg" title="BillySTAT GUI mockup" /></a>

### Creating the GUI

We'd never done anything related to python nor any GUI-developing so all of this is new to us. So naturally we need to read tkinter wiki's and did a bunch of tutorials to get a hang of it.

Resources used:

https://www.youtube.com/watch?v=RJB1Ek2Ko_Y

https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/

https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

https://www.hackanons.com/2018/08/python-3-project-gui-text-editor-using.html

https://docs.python.org/2/library/tkinter.html

http://effbot.org/tkinterbook/place.htm

https://effbot.org/tkinterbook/pack.htm

After testing numerous different ways of creating the GUI we finally made something that resembles our mockup GUI.

<a href="https://i.imgur.com/OSKTQa6.png"><img src="https://i.imgur.com/OSKTQa6.png" title="First GUI" /></a>

[Gif of the GUI](https://giant.gfycat.com/WelcomeBlackAmericanbobtail.webm)

#### Dropdown menu

Like all good applications, BillySTAT needs a dropdown menu too. We wanted the default buttons like Open, Save, Save as and Exit. These were done with the code below.

	self.menu = tki.Menu(window)
        self.window.config(menu=self.menu)

        self.file = tki.Menu(self.menu, tearoff=0)

        self.file.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                              underline=0, command=self.select_source)
        self.file.add_command(label='Save', accelerator='Ctrl+S', compound='left',
                              underline=0, command=self.save)
        self.file.add_command(label='Save as', accelerator='Shift+Ctrl+S',
                              compound='left', command=self.save_statistics)
        self.file.add_command(label='Exit', command=lambda: exit())

        self.menu.add_cascade(label='File', menu=self.file)
	
#### Pushable buttons

To actually make the GUI usefull we need to add some buttons with basic functionality. We wanted buttons like Start Game, Stop Game, Switch Player and Save Statistics. These were made with the code below.

	# START BUTTON
        self.startBtn = tki.Button(window, text="Start game", command=self.startGame)
        self.startBtn.pack(fill=tki.X, pady=11, padx=11)

        # STOP BUTTON
        self.stopBtn = tki.Button(window, text="Stop game", command=self.stopGame)
        self.stopBtn.pack(fill=tki.X, pady=11, padx=11)

        # SWITCH PLAYERS BUTTON
        self.switchBtn = tki.Button(window, text="Switch player", command=self.switchPlayer)
        self.switchBtn.pack(fill=tki.X, pady=11, padx=11)

        # if pressed change player
        # if player1 currently_selected = switch_to_player2
        # if player2 currently_selected = switch_to_player1

        # SAVE STATISTICS BUTTON
        self.saveBtn = tki.Button(window, text="Save game statistics", command=self.save_statistics)
        self.saveBtn.pack(fill=tki.X, pady=11, padx=11)

At this point we still need to attach ***all*** of the functionalities to the GUI. At the moment all of the filedialog prompts are done.

![Test video](https://imgur.com/a/29O8Vdw)

#### Final state of GUI

Unfortunately due to our lack of python and tkinter knowledge we didn't know how to actually connect everything, so we ended up using the GUI to run pallo.py and for selecting the source. 

Final version of the GUI,

<a href="https://i.imgur.com/fDvP2RI.png"><img src="https://i.imgur.com/fDvP2RI.png" title="GUI for BillySTAT" /></a>

### Displaying statistics on screen

Because of not being able to add every functionality in to the GUI we went ahead and wrapped our statistics in the OpenCV output.

To display our variables on screen we used OpenCV:s putText module.

We found [Adrian's People Counter](https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/) really helpful, as he uses cv2.putText on line 245 of his People Counter code.

So we added our own putText,

	info = [
            ("Osuma", osuma),
            ("Ohilyoenti", huti),
            ("Osumisprosentti", osumat),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, 75 - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

This is how it looks like,

<a href="hhttps://i.imgur.com/hZDxVAB.png"><img src="https://i.imgur.com/hZDxVAB.png" title="HUD for BillySTAT's" /></a>

### Saving the statistics

We wanted to have a button with a function that would save the current statistics of the game being played with the push of a button. Our limited knowledge of Tkinter and Python led us to do it the simple way, updating a file called results.txt every iteration of pallo.py with the current statistics.

	results = open('results.txt', 'w')
        results.write("Osumaprosentti ")
        results.write(str(osumat))
        results.write("\n")
        results.write("Osumien määrä ")
        results.write(str(osuma))
        results.write("\n")
        results.write("Ohilyöntien määrä ")
        results.write(str(huti))

<a href="https://i.imgur.com/bH5y8uc.png"><img src="https://i.imgur.com/bH5y8uc.png" title="results.txt" /></a>

The statistics are a bit skewed at the moment because of the lack of black ball recognition, therefore showing up as a missed shot. We're trying to fix it.


## GoPro as the camera

GoPro was the only camera with a field of view broad enough to capture the entire snookertable from the height available to us. Our first thoughts were to use it as a "Webcam" as easily as just pointing it like any other webcam-source, with a 0(default webcam source) or a 1.

	cv2.VideoCapture(0) #or 1

Little did we know, this doesn't work. We either needed a videocapture-card along with a USB-C to HDMI-cable to get it to work and we didn't have the resources for it. Second option for it to work was trying to use it over Wi-Fi wtih [KondradIT's GoProStream tool](https://github.com/KonradIT/GoProStream), which ended up to be too hard to do with our time schedule as we realized this an hour before we went and filmed our validation-game for the project.

We ended up using the GoPro to film a game played by a finnish Semi-Pro Snooker player and analyzing/running it though BillySTAT later.

## Summary

Summary of our project and thoughts about the course.

### YoloV3

YoloV3 would probably work great if we had the time and processing power to create reliable weights that would recognize all balls. Simply put, OpenCV was a better option for us due to the time constraints and our resources. It could quite reliably notice our snooker ballsa and it had great versatility to bend to our needs.

### OpenCV3

OpenCV3 is a great library and you can create very unique things with it. Even though we had no prior Python or Tkinter knowledge, we managed to create BillySTAT, generate statistics with it and had a simple GUI for it.

### BillySTAT



### Thoughts

