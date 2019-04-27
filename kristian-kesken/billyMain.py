# This code is from Adrian Rosebrock's article,
# https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/
# We are using it as GUI-template for our Snooker Statistic tool.

from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import numpy as np

class BillySTATApp:
    def __init__(self):#, cap, outputPath):
        self.cap = cv2.VideoCapture('GOPR0016.MP4')
        #self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None


        # ******** GUI BUTTONS **********
        # START BUTTON
        startBtn = tki.Button(self.root, text="Start game")#, command=self.startGame)
        startBtn.pack(side="top", padx=10, pady=10)

        # STOP BUTTON
        stopBtn = tki.Button(self.root, text="Stop game")#, command=self.stopGame)
        stopBtn.pack(side="top", padx=10, pady=10)

        # SWITCH PLAYERS BUTTON
        switchBtn = tki.Button(self.root, text="Switch player")#, command=self.switchPlayer)
        switchBtn.pack(side="right", padx=10, pady=10)

        # SAVE STATISTICS BUTTON
        saveBtn = tki.Button(self.root, text="Store the statistics and start a new game")#, command=self.saveStatistics)
        saveBtn.pack(side="right", padx=10, pady=10)




        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        #self.stopEvent = threading.Event()
        #self.thread = threading.Thread(target=self.videoLoop, args=())
        #self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("BillySTAT Snooker statistics")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.cap.read()
                self.frame = imutils.resize(self.frame, width=1280)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

   # def startGame(self):
        # start the game
        # TODO ALL

    #def stopGame(self):
        # stop the game
        # TODO ALL

    #def switchPlayer(self):
        # switch the player
        # TODO ALL

    def saveStatistics(self):
        # grab the current timestamp and use it to construct the
        # output path
        # STILL TODO : save the hit/miss % to file
        ts = datetime.datetime.now()
        filename = "{}.txt".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        file.write(p, self.file.copy())
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        #self.stopEvent.set()
        self.cap.release()
        self.root.quit()

bsa = BillySTATApp()
bsa.root.mainloop()
