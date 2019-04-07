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
import math
from collections import deque
import time
import cv2
import numpy as np
import sys

import imutils
from imutils.video import VideoStream


def moving_objects(previous_frame_orig, current_frame_orig, next_frame_orig):

	previous_frame = cv2.cvtColor(previous_frame_orig, cv2.COLOR_BGR2GRAY)
	current_frame = cv2.cvtColor(current_frame_orig, cv2.COLOR_BGR2GRAY)
	next_frame = cv2.cvtColor(next_frame_orig, cv2.COLOR_BGR2GRAY)

	delta_plus = cv2.absdiff(current_frame, previous_frame)
	delta_0 = cv2.absdiff(next_frame, previous_frame)
	delta_minus = cv2.absdiff(current_frame,next_frame)

	sp = cv2.meanStdDev(delta_plus)
	sm = cv2.meanStdDev(delta_minus)
	s0 = cv2.meanStdDev(delta_0)

	th = [
    sp[0][0, 0] + 3 * math.sqrt(sp[1][0, 0]),
    sm[0][0, 0] + 3 * math.sqrt(sm[1][0, 0]),
    s0[0][0, 0] + 3 * math.sqrt(s0[1][0, 0]),
	]

	#ret, dbp = cv2.threshold(delta_plus, th[0], 255, cv2.THRESH_BINARY)
	#ret, dbm = cv2.threshold(delta_minus, th[1], 255, cv2.THRESH_BINARY)
	#ret, db0 = cv2.threshold(delta_0, th[2], 255, cv2.THRESH_BINARY)

	dbp = cv2.adaptiveThreshold(delta_plus, 255, 
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
	dbm = cv2.adaptiveThreshold(delta_minus, 255, 
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
	db0 = cv2.adaptiveThreshold(delta_0, 255, 
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)

	detect = cv2.bitwise_not(
    	cv2.bitwise_and(cv2.bitwise_and(dbp, dbm), 
        cv2.bitwise_not(db0)))

	return detect

testpoints = []

def click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		testpoints.append((x,y))
		print(testpoints)


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

def find_circles(frame, min_radius, max_radius):

	grayframe = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

	#print("went gray")

	circles = cv2.HoughCircles(grayframe,cv2.HOUGH_GRADIENT,1.5,7,
                            param1=100,param2=30,minRadius=min_radius,maxRadius=max_radius)

	#print("got circles")

	if circles is not None:
		circles = np.uint16(np.around(circles))

		for i in circles[0,:]:
			cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
			#print("Putting dots...")
			cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)




# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define color boundaries in 2x hsv

#factor = 255.0/100
gameAreaLower= np.array([52,218,0])
gameAreaUpper= np.array([179,255,255])

gameAreaLower2= np.array([40,0,0])
gameAreaUpper2= np.array([80,255,255])

redLower1=np.array([0,0,0])
redUpper1=np.array([10,255,255])

redLower2=np.array([7,255,56])
redUpper2=np.array([16,99,84])

whiteLower1=np.array([63,0,0])
whiteUpper1=np.array([100,181,255])

blueLower1=np.array([95,178,27])
blueUpper1=np.array([106,255,255])

yellowLower1=np.array([23,0,0])
yellowUpper1=np.array([33,255,255])

greenLower1=np.array([75,229,0])
greenUpper1=np.array([93,255,255])

pinkLower1=np.array([0,0,154])
pinkUpper1=np.array([32,215,255])

blackLower1=np.array([61,0,0])
blackUpper1=np.array([99,255,24])

brownLower1=np.array([15,0,0])
brownUpper1=np.array([57,244,205])

#redLower_1 = np.array([8,100,53])
#redUpper_1 = np.array([14,95,80])

#redLower_2 = np.array([7,100,56])
#redUpper_2 = np.array([16,99,84])

#blueLower1 = np.array([210,88,37])
#blueUpper1 = np.array([205,65,65])

#blueLower2 = np.array([210,88,37])
#blueUpper2 = np.array([205,65,65])

#yellowLower1 = np.array([72,80,58])
#yellowUpper1 = np.array([60,78,100])

#yellowLower2 = np.array([72,80,58])
#yellowUpper2 = np.array([60,78,100])

#greenLower1 = np.array([72,80,58])
#greenUpper1 = np.array([60,78,100])

#greenLower2 = np.array([72,80,58])
#greenUpper2 = np.array([60,78,100])

#pinkLower1 = np.array([72,80,58])
#pinkUpper1 = np.array([60,78,100])

#pinkLower2 = np.array([72,80,58])
#pinkUpper2 = np.array([60,78,100])

#blackLower1 = np.array([72,80,58])
#blackUpper1 = np.array([60,78,100])

#blackLower2 = np.array([72,80,58])
#blackUpper2 = np.array([60,78,100])

#brownLower1 = np.array([53,73,38])
#brownUpper1 = np.array([37,84,63])

#brownLower2 = np.array([61,82,27])
#brownUpper2 = np.array([31,43,62])

# define the size of a single ball
min_area = 150
min_width = 0
max_width = 1000
min_height = 0
max_height = 1000
min_radius = 7
max_radius = 30

pts = deque(maxlen=args["buffer"])

# if not given a video, use webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# video given
else:
	vs = cv2.VideoCapture(args["video"])
#get first valid frame, select polygon points by mouse clicks
frame = vs.read()
frame = vs.read()
frame = frame[1] if args.get("video", False) else frame
if frame is not None:
	frame = imutils.resize(frame, width=1280)
	cv2.imshow("test", frame)
	cv2.setMouseCallback("test", click)
	while True:
		key = cv2.waitKey(1) & 0xFF
		if key == ord("c"):
			cv2.destroyAllWindows()
			break

	area = np.array(testpoints, dtype=np.int32)
#masks out everything else than the polygon points you selected with the mouse
def mask_frame(frame):
	mask = np.zeros((frame.shape[0], frame.shape[1]))
	cv2.fillConvexPoly(mask, area, 1)
	mask = mask.astype(np.bool)
	out = np.zeros_like(frame)
	out[mask] = frame[mask]
	return out, mask

time.sleep(2.0)


def non_color(hsv, Lower1=gameAreaLower2, Upper1=gameAreaUpper2):
	
	mask = cv2.inRange(hsv, Lower1, Upper1)

	mask = ~mask
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.erode(mask, None, iterations=2)

	return mask


def get_contours(frame, hsv, Lower1, Upper1, Lower2=None, Upper2=None):
	# create masks for color "red" 1 + 2
	#mask1 = cv2.inRange(hsv, color_min, color_max)
	#mask1 = cv2.erode(mask1, None, iterations=2)
	#mask1 = cv2.dilate(mask1, None, iterations=2)

	#if range discontinuous

	#mask2 = cv2.inRange(hsv, color_min2, color_max2)
	#mask2 = cv2.erode(mask2, None, iterations=2)
	#mask2 = cv2.dilate(mask2, None, iterations=2)
	
	mask1 = cv2.inRange(hsv, Lower1, Upper1)
	#mask1 = cv2.erode(mask1, None, iterations=2)
	#mask1 = cv2.dilate(mask1, None, iterations=2)

	two_limits = (Lower2 is not None) & (Upper2 is not None)
	
	if two_limits:
		mask2 = cv2.inRange(hsv, Lower2, Upper2)
		#mask2 = cv2.erode(mask2, None, iterations=2)
		#mask2 = cv2.dilate(mask2, None, iterations=2)

	if two_limits:
		mask = mask1 | mask2
	else:
		mask = mask1


	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	center = filter_contours(cnts, min_radius, max_radius)#min_area, min_width, max_width, min_height, max_height)

	if center:
		cv2.circle(frame, center, 5, (0, 0, 255), -1)

	return frame, mask, center

while True:
# current frame

	try:
		prev_frame = unmodified_frame
		frame = next_frame
		next_frame = vs.read()
		next_frame = next_frame[1] if args.get("video", False) else next_frame
	except:
		prev_frame = vs.read()
		frame = vs.read()
		next_frame = vs.read()
		frame = frame[1] if args.get("video", False) else frame
		prev_frame = prev_frame[1] if args.get("video", False) else prev_frame
		next_frame = next_frame[1] if args.get("video", False) else next_frame


# either Video-frame or Cam-frame
	unmodified_frame = frame.copy()
	
	# if no frames left, end
	if (frame is None) or (next_frame is None):
		break
	# resize, blur, convert
	prev_frame = imutils.resize(prev_frame, width=1280)
	frame = imutils.resize(frame, width=1280)
	next_frame = imutils.resize(next_frame, width=1280)

	#testing moving
	det = moving_objects(prev_frame, frame, next_frame)



	frame, framing_mask = mask_frame(frame)
	#blurred = cv2.medianBlur(frame, 7)
	#blurred = cv2.GaussianBlur(frame, (1,1),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#frame, mask, red_center = get_contours(frame, hsv, gameAreaLower2, gameAreaUpper2)

	mask = non_color(hsv)
	mask = framing_mask & mask
	
	abba = cv2.bitwise_and(hsv, hsv, mask=mask)

	#Here is how you can get a single color
	#white = np.zeros_like(frame) 
	#white[:] = np.array([255,255,255])
	#abba = cv2.bitwise_and(white, white, mask=mask)

	blurred = cv2.medianBlur(abba, 3)

	#frame, mask, center = get_contours(frame, blurred, redLower1, redUpper1, redLower2, redUpper2)

	#print(blurred.dtype)
	#blurred = blurred * np.array([1,1,3], dtype=np.uint8)[None, None, :]
	#blurred[blurred > 255] = 255
	#print(np.shape(blurred))
	#print(blurred.dtype)

	find_circles(blurred, min_radius = min_radius, max_radius=max_radius)

	final_frame = cv2.cvtColor(blurred, cv2.COLOR_HSV2BGR)

	grayframe = cv2.cvtColor(cv2.cvtColor(blurred, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)

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
	cv2.imshow("SnookerBall Tracking Frame",det)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	time.sleep(0.02)

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()
