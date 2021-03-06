import cv2
import numpy as np
import time
import os
import glob
from human_detection import HumanDetector


class FrameAnalyzer:
    def __init__(self, threshold=50, cam_name="cam1", img_folder='image_captures/', human_detector=HumanDetector(),
                 human_approaching_threshold=50000, grouping_period=60):
        # threshold sets the min difference between the avg_img and the current frame
        self.threshold = threshold
        self.cam = cam_name
        self.img_folder = img_folder
        self.avg_img = None
        self.human_detector = human_detector  # ML model for humans detection
        self.human_approaching_threshold = human_approaching_threshold  # min size of the detected human in frames
        self.grouping_period = grouping_period  # time period for grouping image captures into folders

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
            # check for any humans detection
            self.human_detection(img)

    def human_detection(self, img):
        """
        Detects for any human motion in the frames
        :param img: current image/frame
        """
        boxes = self.human_detector.detect(img)
        if boxes:
            for i in range(len(boxes)):
                x, y, w, h = boxes[i][1], boxes[i][0], boxes[i][3] - boxes[i][1], boxes[i][2] - boxes[i][0]
                if self.is_approaching_human(w, h):
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    self.save_image(img, time.time())

    def is_approaching_human(self, w, h):
        """
        Detects approaching humans in the frame
        :param w: width of the bounding box around the detected human
        :param h: height of the bounding box around the detected human
        :return: True if the area of the bounding box is greater than the human_approaching_threshold and False otherwise
        """
        return w * h > self.human_approaching_threshold

    def save_image(self, img, img_timestamp):
        """
        Saves and groups the images by consecutive movements captured in the videos
        :param img: current image/frame
        :param img_timestamp: timestamp of when the image was captured
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
            if folder_timestamp - last_timestamp > self.grouping_period:
                os.mkdir(self.img_folder + str(folder_timestamp) + "/")
            else:
                folder_timestamp = last_timestamp

        file_loc = self.img_folder + str(folder_timestamp) + "/" + self.cam + "_" + str(time.time()) + '.jpg'
        cv2.imwrite(file_loc, img)
