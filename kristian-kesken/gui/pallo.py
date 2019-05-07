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

gameAreaLower2 = np.array([40, 0, 0])
gameAreaUpper2 = np.array([80, 255, 255])

# Minimi/maksimi contourin ympäröivän pallon säde että katsotaan pidemmälle.
min_radius = 7
max_radius = 30

# Paljonko saa poiketa ympäröivästä ellipsistä, että hyväksytään palloksi.
area_deviance = 0.30

# Fonttimääritelyjä: https://stackoverflow.com/a/16615935
font = cv2.FONT_HERSHEY_SIMPLEX
fontColor = (255, 255, 255)
lineType = 2

testpoints = []
holes = []


def distance(first, second):
    return np.linalg.norm(first - second)


def others(first_list, second_list, threshold=3):
    # Jos uusi pallo ilmestyy, oletetaan että jotain liikkui, voi olla väärä
    if len(first_list) == 0:
        if len(second_list) != 0:
            return True
        else:
            return False

    for first in first_list:
        distances = np.zeros(len(second_list))
        for index, second in enumerate(second_list):
            distances[index] = distance(first, second)
            # May need to use colors?
        min_distance = np.min(distances)
        if min_distance > threshold:
            return True
        #kaatuu kun others palloja ei ole enään jäljellä, laitettava rauhanomainen lopetus kun other = None
    return False


"""def close_to_holes(past, now, threshold=10):
    global holes

    for ball in past:
        for hole in holes:
            d = distance(np.array(hole), ball)
            # print(np.array(hole), ball, d)
            if d <= threshold:
                return True

    return False"""


white_window = deque([False, False, False], maxlen=3)
other_window = deque([False, False, False], maxlen=3)

shot_in_progress = False
hit = False
huti =0
osuma = 0
yhteensa = 0
osumat = 0.0

def track_hits(white_moved, others_moved, white_location):
    global shot_in_progress
    global white_window
    global other_window
    global hit
    global huti
    global osuma
    global yhteensa
    global osumat


    white_window.append(white_moved)
    other_window.append(others_moved)

    white_true = white_window.count(True)
    other_true = other_window.count(True)

    #white_hole = close_to_holes([white_location], [])

    """if white_hole:
        if shot_in_progress:
            shot_in_progress = False
            print("Virhelyönti")
            print("End shot")
        return"""

    if (white_true == 3) and not (shot_in_progress):
        shot_in_progress = True
        hit = False
        print("Starting shot.")

    if (other_true == 3) and shot_in_progress:
        hit = True

    if (white_true == 0) and shot_in_progress:
        shot_in_progress = False
        if not hit:
            print("Virhelyönti")
            huti += 1
            yhteensa += 1
        else:
            print("Onnistui")
            osuma += 1
            yhteensa += 1
        print("End shot.")

        print(huti)
        print(osuma)
        print(yhteensa)

        osumat = (osuma/yhteensa)*100.0
        print(osumat)
        #label.config(text=osumat[osumat])

# Ottaa controurin määrittelevät pikselit ja ottaa keskiarvon (huom merkityksellinen vain hsv väriavaruudessa)
def mean_color(frame, contour):
    x = contour[:, 0, 0]
    y = contour[:, 0, 1]

    return np.mean(frame[y, x, :], axis=0)


# Lisää klikatun pisteen listaan.
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        testpoints.append((x, y))
        print(testpoints)


def click2bugaloo(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        holes.append((x, y))
        print(("Holes:", holes))


# Katsoo onko kskimääräinen väri annetlla välillä hsv avaruudessa
def colour_filter(color, hsv_low=np.array([30, 10, 200]), hsv_up=np.array([50, 70, 255])):
    if np.all((hsv_low <= color) & (color <= hsv_up)):
        return True
    return False


# Hakee maskista kaikki yhtenäiset alueet, antaa pikselien paikat.
def get_contours(hsv, target, mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    white_location = []
    other_locations = []
    # Valikoidaan aluesita ne mitä ajatelaan palloiksi, ja lasketaan keskimääräinen väri. Plotataan kuvaan.
    for contour in cnts:
        if filter_contours(contour):
            try:
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(target, (cX, cY), 5, (0, 0, 255), -1)
                mcolor = mean_color(hsv, contour)
                if colour_filter(mcolor):
                    cv2.putText(target, "White %s" % mcolor.astype(np.int), (cX, cY), font, 0.5, fontColor,
                                lineType=lineType)
                    white_location = np.array([cX, cY])
                else:
                    cv2.putText(target, "Other %s" % mcolor.astype(np.int), (cX, cY), font, 0.5, fontColor,
                                lineType=lineType)
                    other_locations.append(np.array([cX, cY]))
            except:
                pass

    return target, white_location, other_locations


# Sanoo onko contouri meistä tarpeeksi pallomainen
def filter_contours(contour, min_radius=min_radius, max_radius=max_radius,
                    area_deviance=area_deviance):  # , min_area, min_width, max_width, min_height, max_height):

    (_, radius) = cv2.minEnclosingCircle(contour)

    if radius < min_radius:
        return False

    if radius > max_radius:
        return False

    # Ellipsiä ei voi laskea alle viidestä pikselistä, tuskin on myös pallo jos niin pieni.
    if contour.shape[0] < 5:
        return False

    (x, y), (MA, ma), angle = cv2.fitEllipse(contour)

    area = cv2.contourArea(contour)
    ellipse_area = (math.pi * MA * ma) / 4.0

    fraction = ellipse_area / area

    if fraction > (1.0 + area_deviance):
        return False

    if fraction < (1.0 - area_deviance):
        return False

    return True


# Valitsee kaikki paitsi määritellyn värialueen hsv:stä
def non_color(hsv, Lower1=gameAreaLower2, Upper1=gameAreaUpper2):
    mask = cv2.inRange(hsv, Lower1, Upper1)

    mask = ~mask
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)

    return mask


def main(video=True, name=None):
    print(video, name)
    # if not given a video, use webcam
    if not video:
        vs = VideoStream(src=0).start()
    else:
        vs = cv2.VideoCapture(name)
    # get first valid frame, select polygon points by mouse clicks

    frame = vs.read()

    frame = frame[1] if video else frame
    if frame is not None:
        frame = imutils.resize(frame, width=1280)
        cv2.imshow("test", frame)
        cv2.setMouseCallback("test", click)

        second = False
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):
                cv2.setMouseCallback("test", click2bugaloo)
                if second:
                    cv2.destroyAllWindows()
                    break
                second = True

    area = np.array(testpoints, dtype=np.int32)

    # masks out everything else than the polygon points you selected with the mouse
    def mask_frame(frame):

        mask = np.zeros((frame.shape[0], frame.shape[1]))
        cv2.fillConvexPoly(mask, area, 1)
        mask = mask.astype(np.bool)
        out = np.zeros_like(frame)
        out[mask] = frame[mask]
        return out, mask

    time.sleep(0.5)

    previous = False

    while True:

        frame = vs.read()
        frame = frame[1] if video else frame

        if frame is None:
            break

        frame = imutils.resize(frame, width=1280)

        frame, framing_mask = mask_frame(frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = non_color(hsv)
        mask = framing_mask & mask

        selected = cv2.bitwise_and(hsv, hsv, mask=mask)

        show = cv2.cvtColor(selected, cv2.COLOR_HSV2BGR)

        show, wl, ol = get_contours(hsv, show, mask)

        for location in holes:
            cv2.circle(show, location, 5, (255, 0, 0), -1)

        if previous and (len(wl) != 0):

            white_distance = distance(wl, prev_wl)
            others_moved = others(ol, prev_ol)

            # if close_to_holes(prev_ol, ol):
            # print("A ball went into hole.")

            if white_distance > 1.5:
                white_moved = True
            else:
                white_moved = False

            # print("White moved:",white_moved)
            # print("Others moved:", others_moved)
            track_hits(white_moved, others_moved, prev_wl)

            prev_wl = wl.copy()
            prev_ol = ol.copy()

        else:
            if len(wl) != 0:
                prev_wl = wl.copy()
                prev_ol = ol.copy()
                previous = True

        # show the frame to our screen
        cv2.imshow("SnookerBall Tracking Frame", show)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        time.sleep(0.0005)

    if not video:
        vs.stop()

    else:
        vs.release()

    cv2.destroyAllWindows()


# Mahdollisesti resettaa globalit

if __name__ == "__main__":
    # peruskoodia että nähdään jotain ja saadaan kuva.
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
    args = vars(ap.parse_args())

    # pts = deque(maxlen=args["buffer"])

    main(video=args.get("video", False), name=args["video"])
