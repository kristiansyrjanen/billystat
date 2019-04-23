#edited python3 version of Adrian Rosebrocks code @ https://www.pyimagesearch.com/2016/05/23/opencv-with-tkinter/

from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
from imutils.video import VideoStream
import numpy as np
import time
import math
#import numpy as np

def select_image():
    # grab a reference to the image panels
    global panelA, panelB

    # open a file chooser dialog and allow the user to select an input
    # image
    file = filedialog.askopenfilename(filetypes=(("MP4", "*.mp4;*.m4v;*.f4v;*.mov")
                                                     , ("MPEG-2 TS", "*.mts")
                                                     , ("All files", "*.*")))
    image = cv2.VideoCapture(file)
    # ensure a file path was selected
    if len(file) > 0:
        # load the image from disk, convert it to grayscale, and detect
        # edges in it
        gray = cv2.cvtColor((image), cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)

        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # convert the images to PIL format...
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)

        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)

        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            # while the second panel will store the edge map
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)

            # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

root = Tk()
panelA = None
panelB = None

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select a video", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


root.geometry("300x250+300+300")
root.mainloop()
