import numpy as np
import cv2

img = cv2.imread('pussi2.png',cv2.IMREAD_COLOR)

px = img[55,55]
img[55,55] = [255,255,255]
px = img[55,55]
print(px)
