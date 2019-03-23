import numpy as np
import cv2

img = cv2.imread('/home/matias/tree/pussi2.png',cv2.IMREAD_COLOR)

#img[55,55] = [255,255,255]
#px = img[55,55]

img[100:150, 100:150] [20,20,1]

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows
