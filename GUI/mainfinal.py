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

import matlab.engine

from PIL import Image

#open-source library for wavelet transform https://github.com/PyWavelets/pywt
import pywt
import pywt.data

import dtcwt
import dtcwt.compat
import dtcwt.sampling

from DTCWTLanczos import scale_waveletlanczos
from Bicubic import bicubic_interpolation
import time
from ESRGAN import output_frame
from ESRGAN import output_video
from LocalStruct import LocalStruct

# First the window layout in 2 columns
# pip install "numpy<1.24.0"

directorysave = r'D:\GUI'
filenamesave = 'savedImage.png'

sg.theme('LightGrey1')
# sg. theme_background_color('#DCDCDC')
font = ("Helvetica Bold", 12)
# sg. theme_input_background_color('#DCDCDC')

file_list_column = [
    [
        sg.Text("Video Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(5, 5), key="-FILE LIST-"
        ),
        sg.Text("Choose a video from file list: "),
        sg.Text(size=(40, 1), key="-TOUT-")
    ],
    #[sg.Text("Choose a video from file list")],
    #[sg.Text(size=(40, 1), key="-TOUT-")],
    [
        sg.Text("Original Video Frame Preview", font=font)
    ],
    [
        sg.Image(key="-IMAGE-")
    ],
    [
        sg.Text('Output Image Format'), sg.Combo(['.png', '.jpg', '.bmp'], size=(10, 1), key="-Image Format-"),
        sg.Text('Output Video Format'), sg.Combo(['.mp4', '.avi', '.mov'], size=(10, 1), key="-Video Format-"),
        sg.Text('Output File Name'), sg.Input(key="-FILE NAME-")
    ],
    [
        sg.Text("Choose Start Frame Index:"),
        # sg.Slider(
        #     (0, 240),
        #     0,
        #     1,
        #     orientation="h",
        #     size=(40, 15),
        #     key="-FRAME SLIDER-",
        # ),
        sg.InputText(key="-FRAME SLIDER-"),
        sg.Button("Produce Super-resolved Frame", bind_return_key=True, visible=True)
    ],
    [
        sg.Text("Choose End Frame Index:"),
        # sg.Slider(
        #     (0, 240),
        #     0,
        #     1,
        #     orientation="h",
        #     size=(40, 15),
        #     key="-FRAME SLIDER-",
        # ),
        sg.InputText(key="-END FRAME SLIDER-"),
        sg.Button("Produce Super-resolved Video", bind_return_key=False, visible=True)
    ],
    [sg.Text('Choose Super-resolution Mode'),
     sg.Combo(['Bicubic', 'Structure Adaptation', 'Wavelet', 'Improved NEDI', 'ESRGAN'],
              size=(20, 1), key="-MODE SLIDER-"),
     ],
    [sg.Text("Choose Scaling Ratio"),
     sg.Slider(
         (2, 8),
         2,
         2,
         orientation="h",
         size=(40, 15),
         key="-RATIO SLIDER-",
     ),
     ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Super Resolved Video Frame Preview", font= font)],
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
            and f.lower().endswith((".mp4", ".mov", ".avi"))
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

            imgbytes0 = cv2.imencode(".png", cv2.resize(frame0, (640, 360), interpolation = cv2.INTER_AREA))[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes0)

            #if values["-MODE SLIDER-"] == 0:
                #frame = frame0
            #elif values["-MODE SLIDER-"] == 1:
                #frame = scale_waveletlanczos(frame0, ratio=int(values["-RATIO SLIDER-"]))
            #elif values["-MODE SLIDER-"] == 2:
                #frame = bicubic_interpolation(frame0, scale=int(values["-RATIO SLIDER-"]))

            #imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            #window["-IMAGE-1"].update(data=imgbytes)
        except:
            pass
    if (video != []) and (event == "Produce Super-resolved Frame"):
        # values["-FRAME SLIDER-"] != previous_frame_val) or (values["-MODE SLIDER-"] != previous_mode)

        video.set(cv2.CAP_PROP_POS_FRAMES, int(values["-FRAME SLIDER-"]))
        ret0, frame0 = video.read()
        #frame_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\frame_path\frame0.jpg'
        #cv2.imwrite(frame_path, frame0)

        imgbytes0 = cv2.imencode(".png", cv2.resize(frame0, (640, 360), interpolation = cv2.INTER_AREA))[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes0)

        st = time.time()

        scale = int(values["-RATIO SLIDER-"])
        sg.popup("Processing, Please Wait (Press OK to proceed)")
        if values["-MODE SLIDER-"] == 'Bicubic':
            #bicubic
            frame = cv2.resize(frame0, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            #frame = bicubic_interpolation(frame0, scale=int(values["-RATIO SLIDER-"]))
        elif values["-MODE SLIDER-"] == 'Structure Adaptation':
            frame = LocalStruct(frame0, scale)
        elif values["-MODE SLIDER-"] == 'Wavelet':
            frame = scale_waveletlanczos(frame0, scale=scale)
        elif values["-MODE SLIDER-"] == 'Improved NEDI':
            cv2.imwrite("frame_matlab.png", frame0)
            eng = matlab.engine.start_matlab()
            eng.NEDI_cannybicubic_python(scale)
            eng.quit()
            frame = cv2.imread("NEDIcannybicubic.png")
        elif values["-MODE SLIDER-"] == 'ESRGAN':
            sg.popup("Processing, ratio limited to 4 for SRGAN")
            temp_frame = output_frame(frame0)
            frame = cv2.cvtColor(cv2.imread(r"D:\GUI\sr_frame_path\f.png"), cv2.COLOR_RGB2BGR)



        et = time.time()
        print(et-st)

        print(np.shape(frame))

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-1"].update(data=imgbytes)

        #cv2.imshow("", frame)
        image_path = 'savedImage.png'
        #image_path = 'savedImage.bmp'
        if values["-Image Format-"] == '.jpg' or values["-Image Format-"] == '.bmp' or values["-Image Format-"] == '.png':
            image_path = values["-FILE NAME-"] + values["-Image Format-"]
            #if values["-FILE NAME-"] != []:
                #image_path = values["-FILE NAME-"] + values["-Image Format-"]
        #else:
                #image_path = "savedimage" + values["-Image Format-"]

        cv2.imwrite(image_path, frame)

        sg.popup("Super-resolution Completed. Processed frame saved as " + str(image_path) +  " under " + str(directorysave) + ".")

    elif (video != []) and (event == "Produce Super-resolved Video"):
        video.set(cv2.CAP_PROP_POS_FRAMES, int(values["-FRAME SLIDER-"]))
        ret0, frame0 = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)
        # values["-FRAME SLIDER-"] != previous_frame_val) or (values["-MODE SLIDER-"] != previous_mode)
        frameSize = (frame0.shape[1]*int(values["-RATIO SLIDER-"]), frame0.shape[0]*int(values["-RATIO SLIDER-"]))
        scale = int(values["-RATIO SLIDER-"])

        image_folder = r'D:\GUI'
        video_name = 'video.avi'

        video_path = video_name
        #image_path = 'savedImage.bmp'
        if values["-Video Format-"] == '.mp4' or values["-Video Format-"] == '.avi' or values["-Video Format-"] == '.mov':
            video_path = values["-FILE NAME-"] + values["-Video Format-"]


        #out = cv2.VideoWriter('super_resolved_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(values["-FRAME RATE-"]),
        #                     frameSize)
        #out = cv2.VideoWriter('super_resolved_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), int(values["-FRAME RATE-"]),
        #                     frameSize)
        # video_name = 'super_resolved_video.mp4'
        # out_video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), int(values["-FRAME RATE-"]), frameSize)
        # image_folder = r'C:\Users\jiaqi\PycharmProjects\pythonProject'
        sg.popup("Processing Video, Please Wait. (Press OK to Proceed)")
        if values["-MODE SLIDER-"] == 'ESRGAN':
            output_video(video_path=os.path.join(image_folder, video_path), startframeindex=0, endframeindex=100)
            #SRGAN need to run on Google colab
            #Can run locally but not ideal
        else:
            for frame_index in range(int(values["-FRAME SLIDER-"]), int(values["-END FRAME SLIDER-"])):
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ret0, frame0 = video.read()

                #imgbytes0 = cv2.imencode(".png", frame0)[1].tobytes()
                #window["-IMAGE-"].update(data=imgbytes0)

                #sg.popup("Processing, Please Wait (Press OK to proceed)")

                st = time.time()

                if values["-MODE SLIDER-"] == 'Bicubic':
                    # bicubic
                    frame = cv2.resize(frame0, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                    # frame = bicubic_interpolation(frame0, scale=int(values["-RATIO SLIDER-"]))
                elif values["-MODE SLIDER-"] == 'Structure Adaptation':
                    frame = LocalStruct(frame0, scale)
                elif values["-MODE SLIDER-"] == 'Wavelet':
                    frame = scale_waveletlanczos(frame0, scale=scale)
                elif values["-MODE SLIDER-"] == 'Improved NEDI':
                    cv2.imwrite("frame_matlab.png", frame0)
                    eng = matlab.engine.start_matlab()
                    eng.NEDI_cannybicubic_python(scale)
                    eng.quit()
                    frame = cv2.imread("NEDIcannybicubic.png")


                et = time.time()

                print(et - st)

                print(np.shape(frame))

                cv2.imwrite(str(frame_index)+".png", frame)

                #out.write(frame)

            #image_folder = r'C:\Users\jiaqi\PycharmProjects\pythonProject'

            images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
            frame1 = cv2.imread(os.path.join(image_folder, images[0]))
            height, width, layers = frame1.shape

            #out_video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), int(values["-FRAME RATE-"]), frameSize)
            if values["-Video Format-"] == ".mp4":
                out_video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                            (width, height))
            elif values["-Video Format-"] == ".mov":
                out_video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('X','V','I','D'), fps,
                                            (width, height))
                #hev1
            else:
                out_video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('I','4','2','0'), fps, (width, height))


            for frame_index in range(int(values["-FRAME SLIDER-"]), int(values["-END FRAME SLIDER-"])):
                print(str(frame_index)+".png")
                out_video.write(cv2.imread(os.path.join(image_folder, str(frame_index)+".png")))
                os.remove(os.path.join(image_folder, str(frame_index)+".png"))
            #for image in images:
                #print(image)
                #out_video.write(cv2.imread(os.path.join(image_folder, image)))
                #os.remove(os.path.join(image_folder, image))

            cv2.destroyAllWindows()
            out_video.release()

        #out.release()
        sg.popup("Video Super-resolution Completed. Processed video saved as " + str(video_path) + " under " + str(directorysave) + ".")

        # print(np.shape(converted))
        #cv2.imshow("", frame)
        #cv2.imwrite(filenamesave, frame)
        #sg.popup("Processed Video saved under " + str(directorysave))
        #cv2.imshow("", frame[:, :, 1])
        #cv2.imshow("", frame[:, :, 2])

    previous_frame_val = values["-FRAME SLIDER-"]
    previous_mode = values["-MODE SLIDER-"]

window.close()