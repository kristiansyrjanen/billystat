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

gameAreaLower2= np.array([40,0,0])
gameAreaUpper2= np.array([80,255,255])


#Minimi/maksimi contourin ympäröivän pallon säde että katsotaan pidemmälle.
min_radius = 7
max_radius = 30

#Paljonko saa poiketa ympäröivästä ellipsistä, että hyväksytään palloksi.
area_deviance = 0.30

#Fonttimääritelyjä: https://stackoverflow.com/a/16615935
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontColor              = (255,255,255)
lineType               = 2

testpoints = []

#Ottaa controurin määrittelevät pikselit ja ottaa keskiarvon (huom merkityksellinen vain hsv väriavaruudessa)
def mean_color(frame, contour):
    x = contour[:, 0, 0]
    y = contour[:, 0, 1]

    return np.mean(frame[y,x,:], axis=0)

#Lisää klikatun pisteen listaan.
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        testpoints.append((x,y))
        print(testpoints)

# Katsoo onko kskimääräinen väri annetlla välillä hsv avaruudessa
def colour_filter(color, hsv_low=np.array([30,10,230]), hsv_up=np.array([50,70,255])):
    if np.all((hsv_low <= color) & (color <= hsv_up)):
        return True
    return False

#Hakee maskista kaikki yhtenäiset alueet, antaa pikselien paikat.
#lastWhiteCoordinates = []
currentWhiteCoordinates = []
#lastOtherCoordinates = []
currentOtherCoordinates = []

def get_contours(hsv, target, mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # Valikoidaan aluesita ne mitä ajatelaan palloiksi, ja lasketaan keskimääräinen väri. Plotataan kuvaan.
    for contour in cnts:
        if filter_contours(contour):
            try:
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(target, (cX,cY), 5, (0, 0, 255), -1)
                mcolor = mean_color(hsv, contour)
                if colour_filter(mcolor):
                    cv2.putText(target,"White %s" % mcolor.astype(np.int), (cX, cY), font, 0.5, fontColor, lineType=lineType)
#                    lastWhiteCoordinates.append((cX, cY))
                    currentWhiteCoordinates.append((cX, cY))
                else:
                    cv2.putText(target,"Other %s" % mcolor.astype(np.int), (cX, cY), font, 0.5, fontColor, lineType=lineType)
#                    lastOtherCoordinates.append((cX, cY))
                    currentOtherCoordinates.append((cX, cY))
            except:
                pass

    return target #, currentOtherCoordinates, currentWhiteCoordinates


#Sanoo onko contouri meistä tarpeeksi pallomainen
def filter_contours(contour, min_radius=min_radius, max_radius=max_radius, area_deviance=area_deviance):#, min_area, min_width, max_width, min_height, max_height):

    (_, radius) = cv2.minEnclosingCircle(contour)

    if radius < min_radius:
        return False

    if radius > max_radius:
        return False
    
    #Ellipsiä ei voi laskea alle viidestä pikselistä, tuskin on myös pallo jos niin pieni.
    if contour.shape[0] < 5:
        return False

    (x, y), (MA, ma), angle = cv2.fitEllipse(contour)

    area = cv2.contourArea(contour)
    ellipse_area = (math.pi*MA*ma)/4.0
    
    fraction = ellipse_area/area

    if fraction > (1 + area_deviance):
        return False

    if fraction < (1 - area_deviance):
        return False
    
    return True

#Valitsee kaikki paitsi määritellyn värialueen hsv:stä
def non_color(hsv, Lower1=gameAreaLower2, Upper1=gameAreaUpper2):
	
	mask = cv2.inRange(hsv, Lower1, Upper1)

	mask = ~mask
	mask = cv2.dilate(mask, None, iterations=2)
	mask = cv2.erode(mask, None, iterations=2)

	return mask


#peruskoodia että nähdään jotain ja saadaan kuva.
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])

# if not given a video, use webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
else:
	vs = cv2.VideoCapture(args["video"])
#get first valid frame, select polygon points by mouse clicks

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

time.sleep(0.5)



while True:

    lastWhiteCoordinates, lastOtherCoordinates = currentWhiteCoordinates, currentOtherCoordinates

    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break
    
    frame = imutils.resize(frame, width=1280)

    frame, framing_mask = mask_frame(frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = non_color(hsv)
    mask = framing_mask & mask

    selected = cv2.bitwise_and(hsv, hsv, mask=mask)

    show = cv2.cvtColor(selected, cv2.COLOR_HSV2BGR)

    show = get_contours(hsv, show, mask)
    
    
# show the frame to our screen
    cv2.imshow("SnookerBall Tracking Frame",show)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    time.sleep(0.02)
    
#pallojen liikkuvuuksien vertailua edellisestä ja nykyisesta framesta
print(currentOtherCoordinates)
#lastWhiteCoordinates, lastOtherCoordinates = None
for lastOtherCoordinates in currentOtherCoordinates:
#    firstOther = set(map(tuple, currentOtherCoordinates))
#    secOther = set(map(tuple, lastOtherCoordinates))
#    firstWhite = set(map(tuple, currentWhiteCoordinates))
#    secWhite = set(map(tuple, lastWhiteCoordinates)) 
  
#    other_segment_angles = percentage * 360
    lastOtherCoordinates = currentOtherCoordinates

print(lastOtherCoordinates)
print(currentOtherCoordinates)
    
""" 
currentOtherCoordinates
currentWhiteCoordinates

print(currentOtherCoordinates, lastOtherCoordinates)  


firstOther = set(map(tuple, currentOtherCoordinates))
secOther = set(map(tuple, lastOtherCoordinates))
firstWhite = set(map(tuple, currentWhiteCoordinates))
secWhite = set(map(tuple, lastWhiteCoordinates)) 
other = len(firstOther.symmetric_difference(secOther))
white = len(firstWhite.symmetric_difference(secWhite))
hits = 0
miss = 0
if other != 0:
    hits += 1
else:
    miss += 1
print(miss, hits)
print(firstOther, secOther)

"""

if not args.get("video", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()


#https://www.pythonforengineers.com/image-and-video-processing-in-python/
#https://stackoverflow.com/questions/22876367/how-to-store-last-value-of-iteration