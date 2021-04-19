import cv2
import numpy as np
import time
import os
import glob
from human_detection import HumanDetector


class FrameAnalyzer:
    def __init__(self, threshold=50, cam_name="cam1", img_folder='image_captures/', human_detector=HumanDetector()):
        # threshold sets the min difference between the avg_img and the current frame
        self.threshold = threshold
        self.cam = cam_name
        self.img_folder = img_folder
        self.avg_img = None
        self.human_detector = human_detector  # ML model for human detection

    def motion_detection(self, img):
        """
        Detects any motion in the frame
        :param img: current image being analyzed
        """
        # covert to grayscale and remove noise
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.avg_img is None:
            self.avg_img = gray.astype("float")

        # get any frame changes
        cv2.accumulateWeighted(gray, self.avg_img, 0.5)
        diff_frames = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg_img))
        thresh_frames = cv2.threshold(diff_frames, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh_frames = cv2.dilate(thresh_frames, None, iterations=2)

        if not np.all(thresh_frames == 0):
            # check for any human detection
            self.human_detection(img)

    def human_detection(self, img):
        """
        Uses the TensorFlow Detector API to detect humans in the frames
        :param img: current image/frame
        :return:
        """
        if self.human_detector.is_human(img):
            #print('human detected:' + str(time.time()))
            self.save_image(img, time.time())

    def save_image(self, img, img_timestamp):
        """
        Saves and groups the images by consecutive movements captured in the videos
        """
        # get list of all directories
        dir_list = glob.glob(os.path.join('image_captures/', '*'))
        folder_timestamp = img_timestamp

        if not dir_list:
            os.mkdir(self.img_folder + str(folder_timestamp) + "/")
        else:
            # get the most recent directory created
            recent_dir = max([dir for dir in dir_list], key=os.path.getmtime)
            last_timestamp = float(recent_dir.lstrip().split('/')[-1])
            # create a new folder if more than 60s time passed between the current frame detected and the folder created
            if folder_timestamp - last_timestamp > 60:
                os.mkdir(self.img_folder + str(folder_timestamp) + "/")
            else:
                folder_timestamp = last_timestamp

        file_loc = self.img_folder + str(folder_timestamp) + "/" + self.cam + "_" + str(time.time()) + '.jpg'
        cv2.imwrite(file_loc, img)
