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
from tkinter import filedialog
import threading
import datetime
import pallo

import imutils
from imutils.video import VideoStream


# ******* MAIN WINDOW *********
# root = tki.Tk()
# root.wm_title("BillySTAT Snooker statistics")
class App(tki.Frame):
    def __init__(self, window, window_title, video_source='H:/moniala/gopro1.mp4'):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("280x220+300+300")
        self.video_source = video_source
        # self.vs = MyVideoCapture(self.video_source)


        # ******** GUI BUTTONS *********

        # START BUTTON
        self.startBtn = tki.Button(window, text="Start game", command=self.go_pallo)
        self.startBtn.pack(fill=tki.X, pady=11, padx=11)

        # if pressed and file_selected run pallo.py
        # if file_selected = None
        #     return print("You must select a video before starting a game")

        # STOP BUTTON
        self.stopBtn = tki.Button(window, text="Stop game")  # , command=self.stopGame)
        self.stopBtn.pack(fill=tki.X, pady=11, padx=11)

        # if pressed kill pallo.py destroyAllWindows

        # SWITCH PLAYERS BUTTON
        self.switchBtn = tki.Button(window, text="Switch player")  # , command=self.switchPlayer)
        self.switchBtn.pack(fill=tki.X, pady=11, padx=11)

        # if pressed change player
        # if player1 currently_selected = switch_to_player2
        # if player2 currently_selected = switch_to_player1

        # SAVE STATISTICS BUTTON
        self.saveBtn = tki.Button(window, text="Save game statistics", command=self.save_statistics)
        self.saveBtn.pack(fill=tki.X, pady=11, padx=11)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        # Player 1 hit %

        # Player 2 hit %

        # Menu Bar

        self.menu = tki.Menu(window)
        self.window.config(menu=self.menu)

        self.file = tki.Menu(self.menu, tearoff=0)

        self.file.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                              underline=0, command=self.select_source)
        self.file.add_command(label='Save', accelerator='Ctrl+S', compound='left',
                              underline=0, command=self.save)
        self.file.add_command(label='Save as', accelerator='Shift+Ctrl+S',
                              compound='left', command=self.save_statistics)
        self.file.add_command(label='Exit', command=lambda: exit())

        self.menu.add_cascade(label='File', menu=self.file)

        self.window.mainloop()

    def refresh_label(self):
        """ refresh the content of the label every second """
        self.label.config(text=pallo.osumat)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label.after(1000, self.refresh_label)

    def go_pallo(self):
        pallo.main(video=True, name=self.vs_answer)

    def update(self):
        self.window.after(self.delay, self.update)

    def select_source(self):
        # ask file
        self.vs_answer = filedialog.askopenfilename(parent=self.window,
                                                        defaultextension=".mp4",
                                                        initialdir=os.getcwd(),
                                                        title="Please select a file:",
                                                        filetypes=[('MP4 Files', '*.mp4'),
                                                                   ('M4v Files', '*.m4v'),
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
        self.input_file_name = tki.filedialog.asksaveasfilename(defaultextension=".txt",
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

# Create a window and pass it to the Application object
App(tki.Tk(), "BillySTAT GUI")
