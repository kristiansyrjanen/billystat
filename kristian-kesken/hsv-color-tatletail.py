import cv2 as cv
import numpy as np

#print hsv numbers

red = np.uint8([[[255,0,0 ]]])
hsv_red = cv.cvtColor(red,cv.COLOR_BGR2HSV)
print( hsv_red )
