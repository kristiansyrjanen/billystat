from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import argparse
import time
import math
from collections import deque
import time
import cv2
import os
import numpy as np
import sys
import tkinter as tki
from tkinter import Frame, filedialog, YES, BOTH, Menu
import threading
import datetime

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

file_name = None

delay = 15

# ******* MAIN WINDOW *********
#root = tki.Tk()
#root.wm_title("BillySTAT Snooker statistics")
class App(Frame):
    def __init__(self, window, window_title, video_source='H:/moniala/gopro1.mp4'):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("900x420+300+300")
        self.video_source = video_source

        self.vs = MyVideoCapture(self.video_source)

        self.canvas = tki.Canvas(window)
        self.canvas.pack(expand=YES, fill=BOTH)

        # ******** GUI BUTTONS *********

        # START BUTTON
        self.startBtn = tki.Button(window, text="Start game")  # , command=self.startGame)
        self.startBtn.place(relx=1, x=-55, y=25, anchor=tki.NE)

        # STOP BUTTON
        self.stopBtn = tki.Button(window, text="Stop game")  # , command=self.stopGame)
        self.stopBtn.place(relx=1, x=-55, y=75, anchor=tki.NE)

        # SWITCH PLAYERS BUTTON
        self.switchBtn = tki.Button(window, text="Switch player")  # , command=self.switchPlayer)
        self.switchBtn.place(relx=1, x=-48, y=125, anchor=tki.NE)

        # SAVE STATISTICS BUTTON
        self.saveBtn = tki.Button(window, text="Save game statistics", command=self.save_statistics)
        self.saveBtn.place(relx=1, x=-30, y=175, anchor=tki.NE)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        # Menu Bar

        self.menu = Menu(window)
        self.window.config(menu=self.menu)

        self.file = Menu(self.menu, tearoff=0)

        self.file.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                              underline=0, command=self.select_source)
        self.file.add_command(label='Save', accelerator='Ctrl+S', compound='left',
                              underline=0, command=self.save)
        self.file.add_command(label='Save as', accelerator='Shift+Ctrl+S',
                              compound='left', command=self.save_statistics)
        self.file.add_command(label='Exit', command=lambda: exit())

        self.menu.add_cascade(label='File', menu=self.file)

        self.window.mainloop()

    def update(self):
        ret, frame = self.vs.get_frame()
        frame = imutils.resize(frame, width=720)

        if ret:
            self.image = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.image, anchor=tki.NW)

        self.window.after(self.delay, self.update)

    def select_source(self):
        # ask file
        self.vs_answer = filedialog.askopenfilename(parent=window,
                                                    defaultextension=".mp4",
                                                    initialdir=os.getcwd(),
                                                    title="Please select a file:",
                                                    filetypes=[('MP4 Files', '*.mp4'),
                                                               ('All files', '*.*')])

    def write_to_file(self, file_name):
        try:
            content = content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            tki.messagebox.showwarning("Save", "Could not save the file.")

    def save_statistics(self, event=None):
        # Ask the user to select a single file name for saving.
        self.input_file_name = filedialog.asksaveasfilename(defaultextension=".txt",
                                                            initialdir=os.getcwd(),
                                                            title="Please select a file name for saving:",
                                                            filetypes=[("All Files", "*.*"),
                                                                       ("Text Documents", "*.txt")])
        if self.input_file_name:
            global file_name
            file_name = input_file_name
            write_to_file(file_name)
            window.title('{} - {}'.format(os.path.basename(file_name), window_title))
        return "break"

        """self.filename = name_answer
        self.p = os.getcwd(self.filename)
        self.file.write(p, file.copy())
        print("[INFO] saved {}".format(self.filename))"""

    def save(self, event=None):
        global file_name
        if not file_name:
            save_as()
        else:
            write_to_file(file_name)
        return "break"

def distance(first, second):
    return np.linalg.norm(first - second)

def others(first_list, second_list, threshold=3):
    # Jos uusi pallo ilmestyy, oletetaan että jotain likkuu, voi olla väärä
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

    return False


white_window = deque([False, False, False], maxlen=3)
other_window = deque([False, False, False], maxlen=3)

shot_in_progress = False
hit = False


def track_hits(white_moved, others_moved):
    global shot_in_progress
    global white_window
    global other_window
    global hit

    white_window.append(white_moved)
    other_window.append(others_moved)

    white_true = white_window.count(True)
    other_true = other_window.count(True)

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
        else:
            print("Onnistui")
        print("End shot.")


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


# Katsoo onko keskimääräinen väri annetulla välillä hsv avaruudessa
def colour_filter(color, hsv_low=np.array([30, 10, 230]), hsv_up=np.array([50, 70, 255])):
    if np.all((hsv_low <= color) & (color <= hsv_up)):
        return True
    return False


# Hakee maskista kaikki yhtenäiset alueet, antaa pikselien paikat.
def get_contours(hsv, target, mask):
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    white_location = []
    other_locations = []
    # Valikoidaan alueista ne mitä oletetaan palloiksi, ja lasketaan keskimääräinen väri. Plotataan kuvaan.
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

    if fraction > (1 + area_deviance):
        return False

    if fraction < (1 - area_deviance):
        return False

    return True


# Valitsee kaikki paitsi määritellyn värialueen hsv:stä
def non_color(hsv, Lower1=gameAreaLower2, Upper1=gameAreaUpper2):
    mask = cv2.inRange(hsv, Lower1, Upper1)

    mask = ~mask
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)

    return mask


# peruskoodia että nähdään jotain ja saadaan kuva.
ap = argparse.ArgumentParser()

ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])

# view source
# if not given use webcam
class MyVideoCapture:
    def __init__(self, video_source='H:/moniala/gopro1.mp4'):
        if not False:
            self.vs = cv2.VideoCapture(video_source)
        else:
            self.vs = cv2.VideoCapture(self.select_source)

        self.width = self.vs.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vs.isOpened():
            ret, frame = self.vs.read()
            if ret:
                return(ret,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return(ret, None)

    def __del__(self):
        if self.vs.isOpened():
            self.vs.release()

# get first valid frame, select polygon points by mouse clicks

"""frame = vs.read()

frame = frame[1] if select_source() else frame
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
    frame = frame[1] if False else frame

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

    if previous and (len(wl) != 0):

        white_distance = distance(wl, prev_wl)
        others_moved = others(ol, prev_ol)

        prev_wl = wl.copy()
        prev_ol = ol.copy()

        if white_distance > 1.5:
            white_moved = True
        else:
            white_moved = False

        # print("White moved:",white_moved)
        # print("Others moved:", others_moved)
        track_hits(white_moved, others_moved)

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
    time.sleep(0.02)

if not False:
    vs.stop()

else:
    vs.release()

cv2.destroyAllWindows()"""

# Create a window and pass it to the Application object
App(tki.Tk(), "BillySTAT GUI")
