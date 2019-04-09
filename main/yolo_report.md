YOLOv3 Does not suit for detecting fast small objects 


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

GIFS

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

GIFS 

It turned out that our previous tiny-yolo weights easily outperformed the proper 30k weights. 
We have read about the concept of “overtraining” an AI, where the AI learns the test images so well that it becomes unable to identify anything from new images. 
It is hard to say whether this has happened in our case, but that is what we would look at, had we more time. 
We are very interested in solving this issue, but unfortunately, we simply do not have the time to do so. 
As a result, we had no choice but to drop attempting to work with YOLOv3. 
We believe we can achieve the same things more effectively by building a simple program with OpenCV.
It is proving to be more suitable for detecting fast small objects and allows us to warp the processed image in various ways to ease our future steps, such as calculating and comparing ball and pocket coordinates. 
Next up on our list, is transforming a video image to a 2D image, from which we can hopefully gather and list coordinates.  


