# import packages

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "-buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define color boundaries
redLower = (0,0,255)
redUpper = (255,255,0)
pts = deque(maxlen=args["buffer"])

# if not given a video, use webcam
if not args-get("video", False):
	vs = VideoStream(src=0).start()

# video given
else:
	vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

while True:
	# current frame
	frame = vs.read()
	
	# either Video-frame or Cam-frame
	frame = frame[1] if args.get("video", False) else frame
	
	# if no frames left, end
	if frame is None:
		break
	
	# resize, blur, convert
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GausianBlur(frame, (11,11),0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	# create mask for color "red"
	
	mask = cv2.inRange(hsv, redLower, redUpper)
	mask = cv2.erode(mask, None, iterations = 2)
	mask = cv2.dilate(mask, None, iterations = 2)
	
	# find contours in the mask and initialize the current (x, y) center of ball
	cnts = cv2.findContours(mask.copy(). cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find largest cnt in mask, use it to compute the min enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
		
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame, the update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	
	pts.appendleft(center)
	
	# loop over tracked points
	for i in range(1, len(pts)):
		#if either of the tracked points are None, ignore them
		if pts[i - 1] is None or pts[i] is None:
			continue
		
		#otherwise, compute the thickness fo the line and draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] // float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		
	# show the frame to our screen
	cv2.imshow("SnookerBall Tracking Frame", frame)
	key = cv2.waitKey(i) & 0cFF
	if key == ord("q"):
		break
		
if not args.get("video", False):
	vs.stop()
	
else:
	vs.release()
	
cv2.destroyAllWindows()
