#necessary packages
from time import time, sleep
import numpy as np
import argparse
import cv2

# parse args
"""ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())"""

#list of boundaries
"""boundaries = [
    ([255,255,0], [0,0,255]), # Redball    boundaries 1 point
    ([0,0,0], [0,0,0]),       # Yellowball boundaries 2 points
    ([0,0,0], [0,0,0]),       # Greenball  boundaries 3 points
    ([0,0,0], [0,0,0]),       # Brownball  boundaries 4 points
    ([0,0,0], [0,0,0]),       # Blueball   boundaries 5 points
    ([0,0,0], [0,0,0]),       # Pinkball   boundaries 6 points
    ([0,0,0], [0,0,0])        # Blackball  boundaries 7 points
]"""

cap = cv2.VideoCapture('/home/kristian/topview-snooker.mp4')
ret, current_frame = cap.read()
previous_frame = current_frame

while(cap.isOpened()):
    current_frame_color = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)   # or cv2.COLOR_BGR2HSV, need to test, testet, looks trippy
    previous_frame_color = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2RGB) # or cv2.COLOR_BGR2HSV, need to test, tested, looks trippy

    frame_diff = cv2.absdiff(current_frame_color,previous_frame_color)


    cv2.imshow('frame diff ',frame_diff)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sleep(0.2)
    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()
    
cap.release()
cv2.destroyAllWindows()
