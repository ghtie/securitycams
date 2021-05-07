import cv2
import numpy as np
import time
import os
import glob
from human_detection import HumanDetector


class FrameAnalyzer:
    def __init__(self, threshold=30, cam_name="cam1", img_folder='image_captures/', human_detector=HumanDetector()):
        # threshold sets the min difference between the avg_img and the current frame
        self.threshold = threshold
        self.cam = cam_name
        self.img_folder = img_folder
        self.avg_img = None
        self.human_detector = human_detector  # ML model for human detection
        self.human_approaching_threshold = 30000

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
            return self.human_detection(img)
        return None

    def human_detection(self, img):
        """
        Uses the model classifier to detect humans in the frames and create image captures
        :param img: current image/frame
        """
        boxes = self.human_detector.detect(img)
        if boxes:
            for i in range(len(boxes)):
                x, y, w, h = boxes[i][1], boxes[i][0], boxes[i][3] - boxes[i][1], boxes[i][2] - boxes[i][0]
                if self.is_approaching_human(w, h):
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    self.save_image(img, time.time())
                    cv2.putText(img, 'APPROACHING HUMAN', (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                else:
                    cv2.putText(img, 'PASSING HUMAN', (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        else:
            cv2.putText(img, 'MOTION DETECTED', (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        return img

    def is_approaching_human(self, w, h):
        """
        Calculates the area of the bounding box around the detected human in the frame
        :return: True if the human is approaching the camera
        """
        # print(w * h)
        return w * h > self.human_approaching_threshold

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
