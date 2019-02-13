

<!-- toc -->

- [BillySTAT](#billystat)
  * [School project @Haaga-Helia University of Applied Sciences](#school-project-haaga-helia-university-of-applied-sciences)
    + [Project members](#project-members)
    + [Things to do](#things-to-do)
  * [Setting up environment for YOLOv3](#setting-up-environment-for-yolov3)
    + [Installations](#installations)
      - [Nvidia drivers](#nvidia-drivers)
      - [CUDA installation](#cuda-installation)
      - [OpenCV3](#opencv3)

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
+ ~~Setup server~~
+ ~~Install CUDA, OpenCV3, Darknet and YOLOv3~~
+ ~~Run basic tests~~
+ Train YOLOv3
+ Make it recognise only things relevant
+ Create boundaries that when crossed, counts as a point/points depending what colored ball it is.
+ Make it count statistics
+ Create GUI for statistics

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

### Installations
#### Nvidia drivers
First off we'll download NVidia drivers, let's start by adding nvidia ppa:latest,

    sudo add-apt-repository ppa:graphics-drivers
    sudo apt-get update

Install Nvidia drivers,

    sudo apt-get install nvidia-driver-410

And reboot

    sudo reboot
    
#### CUDA installation

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

#### OpenCV3
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

#### Installing Darknet

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

### Training your neural networks

#### Creating training material

#### Resizing images

To resize the images to a smaller size we made a script thadoes it for us, let's call it *resize.sh*:

	FOLDER="/path/to/images"

	WIDTH=800

	HEIGHT=600

	find ${FOLDER} -iname '*.jpg' -exec convert \{} -verbose -resize $WIDTHx$HEIGHT\> \{} \;

Run it,

	./resize.sh # Or bash resize.sh, make sure you have x-rights correct
##### 1st Alternative: YOLO-Annotation-Tool

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


##### 2nd Alternative: Open Labeling

We also tried another labeling-tool called [Open Labeling](https://github.com/Cartucho/OpenLabeling).

	git clone https://github.com/Cartucho/OpenLabeling.git

You can install everything at once by simply running:

	python -mpip install -U pip
	python -mpip install -U -r requirements.txt

Ran the program, shut it down and tried reopening it again and was greeted by Error messages. That was the first and last time we got it to work.

##### 3rd Alternative: Yolo_mark by AlexeyAB

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



#### Add weights to YOLOv3


#### Testing frame difference from video

##### Virtualenv

Either use earlier facecourse-py3 virtualenv or create a new one with suiting name.

We created a new one, *billystat*, the same way as the facecourse virtualenv.

	mkvirtualenv billystat -p python3
	workon billystat
	
	pip install numpy scipy matplotlib scikit-image scikit-learn ipython
	deactivate

Create symlink
	
	cd ~/.virtualenvs/billystat/lib/python3.6/site-packages
	ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so

##### Frame diff from video with grayscale

	workon billystat
	
	python3 billyFRAME.py
	
![Alt Text](https://i.imgur.com/QO2VE2P.gif)
