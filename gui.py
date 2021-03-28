import time
import os
import cv2
import PySimpleGUI as sg
import pathlib

# init Windows Manager
sg.theme("DarkBlue")

# def webcam col
colwebcam1_layout = [[sg.Text("Camera View 1", size=(60, 1), justification="center")],[sg.Image(filename="", key="cam1")]]
colwebcam1 = sg.Column(colwebcam1_layout, element_justification='center')

colwebcam2_layout = [[sg.Text("Camera View 2", size=(60, 1), justification="center")],
                     [sg.Image(filename="", key="cam2")]]
colwebcam2 = sg.Column(colwebcam2_layout, element_justification='center')
colslayout = [colwebcam1, colwebcam2]

rowfooter = [sg.Image(filename="", key="-IMAGEBOTTOM-")]
layout = [colslayout,
        rowfooter,
        [sg.FileBrowse(button_text="See Images Displaying Motion", font=('any', 16), initial_folder=pathlib.Path().absolute() / 'image_captures')],
        [sg.Text("Log of Detected Motion", font=('any', 25))],
        [sg.Multiline("---- MOTION DETECTION LOG ---\n", size = (97, 25), font=('any', 16), key="LOG")]]

right_click_menu = ['Unused', ['&FPS', '---', 'Menu A', 'Menu B', 'Menu C', ['Menu C1', 'Menu C2'], '---', 'Exit']]

window = sg.Window("Security Cameras", layout,
                   right_click_menu=right_click_menu,
                   no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                   return_keyboard_events=True, location=(100, 100), finalize=True)

# populate the initial motion log
directory = pathlib.Path().absolute() / 'image_captures'
files = set(os.listdir(directory))
for filename in files:
    if filename.endswith(".jpg") or filename.endswith(".png"):
        l = filename.split('_')
        window["LOG"].print(l[0] + ' detected motion at ' + l[1].split('.')[0])

# Camera Settings
camera_Width = 480  # 640 # 1024 # 1280
camera_Heigth = 320  # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)
video_capture = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(2)
time.sleep(2.0)

display_fps = False
while True:
    start_time = time.time()

    # process windows events
    event, values = window.read(timeout=20)
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "f" or event == "F" or event == "FPS":
        display_fps = not display_fps

    # get camera frame
    ret, frameOrig = video_capture.read()
    frame = cv2.resize(frameOrig, frameSize)

    ret2, frameOrig2 = video_capture2.read()
    frame2 = cv2.resize(frameOrig2, frameSize)

    if (display_fps == True) and (time.time() - start_time) > 0:
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)

    # update webcam1
    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["cam1"].update(data=imgbytes)

    # update webcam2
    imgbytes2 = cv2.imencode(".png", frame2)[1].tobytes()
    window["cam2"].update(data=imgbytes2)

    #update Motion detection log
    # todo compare files set to set at time of loop, print diff

video_capture.release()
video_capture2.release()
cv2.destroyAllWindows()
