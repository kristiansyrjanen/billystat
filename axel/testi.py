import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
from __future__ import division

def find_sportsball(image):
	#Color scheme convertion
	image = cv2.cvtColor(image, cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	#Scale
	max_dimension = max(image.shape)
	scale = 700/max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)
	#Cleaning image
	image_blur = cv2.GaussianBlur(image, (7,7), 0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
	#Filters
	min_red= np.array([0,100, 80])
	max_red= np.array([10,256, 256])
	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)

	min_red2 = np.array([170,100,80])
	max_red2 = np.array([180,256,256])
	mask2 = cv2.inRange
