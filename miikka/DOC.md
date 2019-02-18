## BillySTAT custom object training notes

### Before beginning, make sure you have your OpenCV/Darknet environment set up. Your exact directory structure may wary, keep that in mind.

!! By this point you should have your neural network environment setup. Make sure you are able to run some detection tests from images or videos. If that doesn't work, this won't either. !!

# Prerequisites

Let's start by copying and editing our config file:
	
	cp darknet/cfg/yolov3.cfg ../yolo-obj.cfg

Edit the line **batch** to **batch=64**.

Edit the line **subdivisions** to **subdivisions=64**. If your GPU has lots of memory (over 4GB), you can lower the subdivision number to 32, 16 or even 8. 

Edit the line number 610 **classes** to whatever the amount of objects you want to detect is. For example, if you have 10 colors you wish to detect, you have 10 objects and as such, 10 classes. The line would be **classes=10**

Do the same for lines 696 and 783 as well.

Edit the line number 603 **filters** to whatever your amount of objects + 5 and multiply it by 3. (Objects+5)x3. For example, with 10 objects the correct filter value would be 45. 10 + 5 = 15 * 3 = 45.

Do the same for lines 689 and 776 as well.

After this, create file **obj.names** in your darknet directory.

Write the names of all your objects you want to detect, each in their own line.

For example, if we wanted to detect colors, we would start listing: 1. Green, 2. Blue, 3. Yellow, and so on. **Make sure each object is in their own line.**

Next, create file **obj.data**. In it, fill the following information:

	classes= 10 //the number of your objects
	train = train.txt //you can change these paths if your directory structure differs
	valid = train.txt //^
	names = obj.names
	backup = backup/ //this is where backups of weights files are made, every 1000 lines I think.


# Marking the images

Now comes the boring part. Make sure you have all your teaching material (.jpgs) ready in a single folder. Download this lovely tool made by AlexeyAB:

	https://github.com/AlexeyAB/Yolo_mark

Yolo_mark allows us to mark the "interesting bits" of the pictures to the AI. The tool may seem a bit broken or lazily made, but trust us, it seems to be the best one out there.

On the other hand, if you want to do it by hand, you can measure the the exact pixel positions of the "interesting bits" and write the files yourself. But this is akin to suicide, don't do it.

You can find more material and directions about this tool from the main README file of this repo, written by Kristian. 

When you are done, you should have your images in a single folder, each with their accompanying .txt file. 

# Actual training - Please note: This section is still a work in progress. Things may change and, put simply, be completely wrong at any point. We are still working out the best settings to yield the best results. 

Once marking is done, copy **obj.data**, **obj.names** and **train.txt** to your main darknet folder. (Or wherever you want, make sure you remember it)

Now, open *train.txt**, and make sure it contains the location of every image. One image per line. Yolo_mark should create the file, but if you want to change the image location, you can do it here.

For example, if all your images are in darknet/test:

	test/1.jpg
	test/2.jpg
	test/...

Great! Now before we can try training, we still need to download the premade training weights from the official site:

	$ wget http://pjreddie.com/media/files/darknet53.conv.74

And now, if you're feeling confident, we can finally attempt training:

	./darknet detector train obj.data yolo-obj.cfg darknet53.conv.74

If all goes well, you should start seeing lots of numbers:

![Alt Text](https://i.imgur.com/k3sXNi0.gif)

Is text flashing before your eyes? Great! Do you see lots of -nan? Maybe not great, who knows at this point. This is what we are trying to find out. At the moment of writing, we  believe that some nans are tolerable, but you should start seeing less and less the longer you train.

If you run into CUDA memory errors, try editing the **yolo-obj.cfg** file. Worst case scenario, edit subdivions and batch to 64. You can also try editing the image dimensions, however keep in mind that they **must** be divisible by 32. Make a note of the original values, so you can return to them if things go wrong.

On low memory setups, you can try copying the yolov3-tiny.cfg file from the cfg folder and making the same adjustments to it as you made to the original yolov3 cfg. Training the tiny version requires 1 GB of memory, so keep that in mind. 

Stay tuned for more, next we will look at using our trained files for something useful, such as detecting objects from videos! Cool!
