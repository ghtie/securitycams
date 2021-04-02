import time
import os
import cv2
import PySimpleGUI as sg
import pathlib


def log_movement(window, old_set, new_set):
    directory = pathlib.Path().absolute() / 'image_captures'
    print(new_set)
    for filename in (new_set - old_set):
        l = filename.split('.')
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(l[0])))
        window["LOG"].print('Detected motion at ' + date)


def main():
    # init Windows Manager
    sg.theme("DarkBlue")

    # def webcam col
    col_webcam1_layout = [[sg.Text("Camera View 1", size=(60, 1), justification="center")],
                         [sg.Image(filename="", key="cam1")]]
    col_webcam1 = sg.Column(col_webcam1_layout, element_justification='center')

    col_webcam2_layout = [[sg.Text("Camera View 2", size=(60, 1), justification="center")],
                         [sg.Image(filename="", key="cam2")]]
    col_webcam2 = sg.Column(col_webcam2_layout, element_justification='center')
    cols_layout = [col_webcam1, col_webcam2]

    directory = pathlib.Path().absolute() / 'image_captures'
    footer = [sg.Image(filename="", key="-IMAGEBOTTOM-")]
    layout = [cols_layout,
              footer,
              [sg.FileBrowse(button_text="See Images Displaying Motion", font=('any', 16), initial_folder=directory)],
              [sg.Text("Log of Detected Motion", font=('any', 25))],
              [sg.Multiline("---- MOTION DETECTION LOG ---\n", size=(97, 25), font=('any', 16), key="LOG")]]

    right_click_menu = ['Unused', ['&FPS', '---', 'Menu A', 'Menu B', 'Menu C', ['Menu C1', 'Menu C2'], '---', 'Exit']]

    window = sg.Window("Security Cameras", layout,
                       right_click_menu=right_click_menu,
                       no_titlebar=False, alpha_channel=1, grab_anywhere=False,
                       return_keyboard_events=True, location=(100, 100), finalize=True)

    # populate the initial motion log
    files = set([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])
    log_movement(window, set(), files)

    # Camera Settings
    camera_width = 480  # 640 # 1024 # 1280
    camera_height = 320  # 480 # 780  # 960
    frame_size = (camera_width, camera_height)
    video_capture = cv2.VideoCapture(1)
    video_capture2 = cv2.VideoCapture(0)
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
        ret, frame_orig = video_capture.read()
        frame = cv2.resize(frame_orig, frame_size)

        ret2, frame_orig2 = video_capture2.read()
        frame2 = cv2.resize(frame_orig2, frame_size)

        if (display_fps == True) and (time.time() - start_time) > 0:
            fps_info = "FPS: " + str(1.0 / (time.time() - start_time))  # FPS = 1 / time to process loop
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, fps_info, (10, 20), font, 0.4, (255, 255, 255), 1)

        # update webcam1
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["cam1"].update(data=imgbytes)

        # update webcam2
        imgbytes2 = cv2.imencode(".png", frame2)[1].tobytes()
        window["cam2"].update(data=imgbytes2)

        #update Motion detection log
        files_new = set([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])
        log_movement(window, files, files_new)
        files = files_new

    video_capture.release()
    video_capture2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
