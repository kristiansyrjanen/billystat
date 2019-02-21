#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin

green = (0, 255, 0)

def show(image):
	plt.figure(figsize=(10, 10))
	plt.imshow(image, interpolation='nearest')
def overlay_mask(mask, image):
	rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
	img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
	return img
def find_redballs(image):
	image = image.copy()
	image, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	mask = np.zeros(image.shape, np.uint8)
	#Ei tarvitse tehdä hakua isoimmasta, koska haluan kaikki punaiset pallot
	cv2.drawContours(mask, contours, -1, 255, -1)
	return contours, mask

def circle_contour(image, contour):
	image_with_ellipse = image.copy()
	ellipse = cv2.fitEllipse(contour)
	cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.LINE_AA)
	return image_with_ellipse

def find_sportsball(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	max_dimension = max(image.shape)
	scale = 700/max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)
	image_blur = cv2.GaussianBlur(image, (7,7), 0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
	min_red= np.array([0,100, 80])
	max_red= np.array([10,256, 256])
	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)
	min_red2 = np.array([170,100,80])
	max_red2 = np.array([180,256,256])
	mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
	mask = mask1 + mask2
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
	mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
	all_sportsball_contour, mask_sportsball = find_redballs(mask_clean)
	overlay = overlay_mask(mask_clean, image)
	circled = overlay
	#Jokaiselle contourille piirretään samaan kuvaan ympyrä
	for contour in all_sportsball_contour:
		circled = circle_contour(circled, contour)
	show(circled)
	bgr = cv2.cvtColor(circled, cv2.COLOR_RGB2BGR)
	return bgr
	
image =cv2.imread('testi.jpg')
result = find_sportsball(image)
			     
cv2.imwrite('testi2.jpg', result)
