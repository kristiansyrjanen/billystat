#!/usr/bin/env python3
import time
import cv2
from display import Display

W = 1920//2
H = 1080//2

disp = Display(W, H)
orb = cv2.ORB_create()
print(dir(orb))
class FeatureExtractor(object):
    GX =

def process_frame(img):
    img = cv2.resize(img, (W,H))

    surf = pygame.surfarray.make_surface(img)
    screen.blit(surf, (0,0))
    pygame.display.flip()

    print(img.shape)

if __name__ == "__main__":
    cap = cv2.VideoCapture("topview-snooker.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            process_frame(frame)
        else:
            break
