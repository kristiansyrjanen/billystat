### BillySTAT custom object training notes

## Before beginning, make sure you have your OpenCV/Darknet environment set up. Your exact directory structure may wary, keep that in mind.

By this point you should have your neural network environment setup. Make sure you are able to run some detection tests from images or videos. If that doesn't work, this won't either.

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

Now comes the boring part. Make sure you have all your teaching material (.jpgs) ready in a single folder. Download this lovely tool made by AlexeyAB:

	https://github.com/AlexeyAB/Yolo_mark

Yolo_mark allows us to mark the "interesting bits" of the pictures to the AI. The tool may seem a bit broken or lazily made, but trust us, it seems to be the best one out there.

On the other hand, if you want to do it by hand, you can measure the the exact pixel positions of the "interesting bits" and write the files yourself. But this is akin to suicide, don't do it.

You can find more material and directions about this tool from the main README file of this repo, written by Kristian. 

When you are done, you should have your images in a single folder, each with their accompanying .txt file. 

