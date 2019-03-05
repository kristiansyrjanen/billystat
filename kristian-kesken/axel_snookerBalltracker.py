# Adrian Rosebrock's ball tracking code variant
# https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

#Things to do 4.3.2019:
#Define colors for each ball
#Define ball sizes in current material aka smallest and biggest from each ball
#Do loop for each different ball (red excluded)
#Save coordinates in some structure

#After these we can start thinking about what we do with our information and how to deal with red balls

# import packages

import argparse
import time
from collections import deque
import time
import cv2
import numpy as np

import imutils
from imutils.video import VideoStream

#Returns the first center point of a ball that passes all the tests
def filter_contours(input_contours, min_radius, max_radius):#, min_area, min_width, max_width, min_height, max_height):

	center= ()
	x=0
	y=0
	for contour in input_contours:

		(_, radius) = cv2.minEnclosingCircle(contour)

		if radius < min_radius:
			continue

		if radius > max_radius:
			continue

		# x,y,w,h = cv2.boundingRect(contour)
		
		# if (w < min_width or w > max_width):
		# 	continue
		# if (h < min_height or h > max_height):
		# 	continue
		# area = cv2.contourArea(contour)
		# if (area < min_area):
		# 	continue

		M = cv2.moments(contour)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		x=cX
		y=cY
		center = (x,y)
		break

	return center

# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define color boundaries in 2x hsv
redLower_1 = np.array([170, 70, 50])
redUpper_1 = np.array([180, 255, 255])

redLower_2 = np.array([0, 70, 50])
redUpper_2 = np.array([10, 255, 255])

blueLower1 = np.array([210,88,37])
blueUpper1 = np.array([205,65,65])

blueLower2 = np.array([210,88,37])
blueUpper2 = np.array([205,65,65])

yellowLower1 = np.array([72,80,58])
yellowUpper1 = np.array([60,78,100])

yellowLower2 = np.array([72,80,58])
yellowUpper2 = np.array([60,78,100])

greenLower1 = np.array([72,80,58])
greenUpper1 = np.array([60,78,100])

greenLower2 = np.array([72,80,58])
greenUpper2 = np.array([60,78,100])

pinkLower1 = np.array([72,80,58])
pinkUpper1 = np.array([60,78,100])

pinkLower2 = np.array([72,80,58])
pinkUpper2 = np.array([60,78,100])

blackLower1 = np.array([72,80,58])
blackUpper1 = np.array([60,78,100])

blackLower2 = np.array([72,80,58])
blackUpper2 = np.array([60,78,100])

brownLower1 = np.array([72,80,58])
brownUpper1 = np.array([60,78,100])

brownLower2 = np.array([72,80,58])
brownUpper2 = np.array([60,78,100])

# define the size of a single ball
min_area = 150
min_width = 0
max_width = 1000
min_height = 0
max_height = 1000
min_radius = 20
max_radius = 100

pts = deque(maxlen=args["buffer"])

# if not given a video, use webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# video given
else:
	vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

def get_contours(frame, hsv, color_min, color_max, color_min2, color_max2):
	# create masks for color "red" 1 + 2
	mask1 = cv2.inRange(hsv, color_min, color_max)
	mask1 = cv2.erode(mask1, None, iterations=2)
	mask1 = cv2.dilate(mask1, None, iterations=2)

	#if range discontinuous

	mask2 = cv2.inRange(hsv, color_min2, color_max2)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	mask = mask1 | mask2

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	center = filter_contours(cnts, min_radius, max_radius)#min_area, min_width, max_width, min_height, max_height)

	if center:
		cv2.circle(mask, center, 5, (0, 0, 255), -1)

	return mask, center

while True:
# current frame
	frame = vs.read()
	
# either Video-frame or Cam-frame
	frame = frame[1] if args.get("video", False) else frame
	
	# if no frames left, end
	if frame is None:
		break
	# resize, blur, convert
	frame = imutils.resize(frame, width=1280)
	blurred = cv2.GaussianBlur(frame, (11,11),0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	mask, red_center = get_contours(frame, hsv, redLower_1, redUpper_1, redLower_2, redUpper_2)

	# # create masks for color "red" 1 + 2
	# mask1 = cv2.inRange(hsv, redLower_1, redUpper_1)
	# mask1 = cv2.erode(mask1, None, iterations=2)
	# mask1 = cv2.dilate(mask1, None, iterations=2)

	# mask2 = cv2.inRange(hsv, redLower_2, redUpper_2)
	# mask2 = cv2.erode(mask2, None, iterations=2)
	# mask2 = cv2.dilate(mask2, None, iterations=2)

	# mask = mask1 | mask2


	


	# # find contours in the mask and initialize the current (x, y) center of ball
	# cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# cnts = imutils.grab_contours(cnts)
	# center = None

	# # only proceed if at least one contour was found
	# if len(cnts) > 0:
	# 	for c in cnts:
	# 		# find largest cnt in mask, use it to compute the min enclosing circle and centroid
	# 		#c = max(cnts, key=cv2.contourArea)
	# 		((x, y), radius) = cv2.minEnclosingCircle(c)
	# 		M = cv2.moments(c)
	# 		center = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
		
	# 		# only proceed if the radius meets a minimum size
	# 		if radius > 10:
	# 			# draw the circle and centroid on the frame, the update the list of tracked points
	# 			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
	# 			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# 			#Printtaa punaisen alueen keskipisteen koordinaatit
	# 			print(x, y)

	# pts.appendleft(center)

	# # loop over tracked points
	# for i in range(1, len(pts)):
	# 	#if either of the tracked points are None, ignore them
	# 	if pts[i - 1] is None or pts[i] is None:
	# 		continue
	
	# 	#otherwise, compute the thickness fo the line and draw the connecting lines
	# 	thickness = int(np.sqrt(args["buffer"] // float(i + 1)) * 2.5)
	# 	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

# show the frame to our screen
	cv2.imshow("SnookerBall Tracking Frame", mask)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	time.sleep(0.02)

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()
