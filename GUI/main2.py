# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# img_viewer.py
# pyinstaller --onefile img_viewer.py

import PySimpleGUI as sg
import os
import os.path
import cv2

import numpy as np
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt

from PIL import Image

#open-source library for wavelet transform https://github.com/PyWavelets/pywt
import pywt
import pywt.data

import dtcwt
import dtcwt.compat
import dtcwt.sampling

from DTCWTLanczos import scale_waveletlanczos



# First the window layout in 2 columns

directorysave = r'D:\GUI'
filenamesave = 'savedImage.jpg'


file_list_column = [
    [
        sg.Text("Video Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(5, 5), key="-FILE LIST-"
        )
    ],
    [sg.Text("Choose a video from file list")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
    [
        sg.Text("Choose Frame Index:"),
        # sg.Slider(
        #     (0, 240),
        #     0,
        #     1,
        #     orientation="h",
        #     size=(40, 15),
        #     key="-FRAME SLIDER-",
        # ),
        sg.InputText(key="-FRAME SLIDER-"),
    ],
    [sg.Text("Choose Super-resolution mode"),
     sg.Slider(
         (0, 1),
         0,
         1,
         orientation="h",
         size=(40, 15),
         key="-MODE SLIDER-",
     ),
     ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Super Resolved Video Frame")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    # [sg.Image(key="-IMAGE-")],
    [sg.Image(filename="", key="-IMAGE-1")],
]


# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Video Upscaler", layout)

# cap = cv2.VideoCapture(0)

# Run the Event Loop

video = []


while True:
    event, values = window.read(timeout=20)
    # ret, frame = cap.read()


    #if video != []:
        #ret0, frame0 = video.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".mp4"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)

            video = cv2.VideoCapture(filename)
            fps = video.get(cv2.CAP_PROP_FPS)
            pos_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
            video.set(cv2.CAP_PROP_POS_FRAMES, int(values["-FRAME SLIDER-"]))

            ret0, frame0 = video.read()

            imgbytes0 = cv2.imencode(".png", frame0)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes0)

            if values["-MODE SLIDER-"] == 0:
                frame = frame0
            elif values["-MODE SLIDER-"] == 1:
                frame = scale_waveletlanczos(frame0)

            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-1"].update(data=imgbytes)

        except:
            pass
    if (video != []) and ((values["-FRAME SLIDER-"] != previous_frame_val) or (values["-MODE SLIDER-"] != previous_mode)):
        video.set(cv2.CAP_PROP_POS_FRAMES, int(values["-FRAME SLIDER-"]))
        ret0, frame0 = video.read()

        imgbytes0 = cv2.imencode(".png", frame0)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes0)

        if values["-MODE SLIDER-"] == 0:
            frame = frame0
        elif values["-MODE SLIDER-"] == 1:
            sg.popup("Processing, Please Wait (Press OK to proceed)")
            frame = scale_waveletlanczos(frame0)

        print(np.shape(frame))
        sg.popup("Super-resolution Completed")
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-1"].update(data=imgbytes)

        converted = frame[:, :, (1, 2, 0)]
        # print(np.shape(converted))
        cv2.imshow("", frame)
        cv2.imwrite(filenamesave, frame)
        sg.popup("Processed frame saved as image under " + str(directorysave))
        #cv2.imshow("", frame[:, :, 1])
        #cv2.imshow("", frame[:, :, 2])

    previous_frame_val = values["-FRAME SLIDER-"]
    previous_mode = values["-MODE SLIDER-"]

window.close()