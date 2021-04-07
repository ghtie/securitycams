import cv2
import imutils
import numpy as np
import time
import os
import glob
from human_detection import HumanDetector


class FrameAnalyzer:
    def __init__(self, threshold=50, cam_name="cam1", img_folder='image_captures/', human_detector=HumanDetector(), model_threshold=0.7):
        # threshold sets the min difference between the avg_img and the current frame
        self.threshold = threshold
        self.cam = cam_name
        self.img_folder = img_folder
        self.avg_img = None
        self.human_detector = human_detector  # ML model for human detection
        self.model_threshold = model_threshold

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
        img = cv2.resize(img, (1280, 720))
        boxes, scores, classes = self.human_detector.obj_detection(img)

        # # Filter for only human detection
        # human_idx = np.argwhere(np.array(classes) == 1)  # Class 1 = Human
        # boxes = np.array(boxes)[human_idx]
        # scores = np.array(scores)[human_idx]

        for i in range(len(boxes)):
            # Class 1 = Humans
            if classes[i] == 1 and scores[i] > self.model_threshold:
                print("Human detected at: " + str(time.time()))
                box = boxes[i]
                cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                self.save_image(img)

    def img_capture(self, img, thresh_frames):
        """
        Creates screenshots from frames that have detected motion
        :param img: current image/frame being analyzed
        :param thresh_frames: ndarray of image pixels
        """
        contours = cv2.findContours(thresh_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        for contour in contours:
            if cv2.contourArea(contour) > 5000:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # create screenshots for user to review later
                self.save_image(img)

    def save_image(self, img):
        """
        Saves and groups the images by consecutive movements captured in the videos
        """
        # get list of all directories
        dir_list = glob.glob(os.path.join('image_captures/', '*'))
        curr_time = time.time()
        timestamp = ""
        if not dir_list:
            timestamp = time.time()
            os.mkdir(self.img_folder + str(timestamp) + "/")
        else:
            # get the most recent directory created
            recent_dir = max([dir for dir in dir_list], key=os.path.getmtime)
            last_timestamp = float(recent_dir.lstrip().split('/')[-1])
            # create a new folder if more than 10s time passed between the current frame detected and the folder created
            if curr_time - last_timestamp > 10:
                timestamp = curr_time
                os.mkdir(self.img_folder + str(timestamp) + "/")
            else:
                timestamp = last_timestamp

        file_loc = self.img_folder + str(timestamp) + "/" + self.cam + "_" + str(time.time()) + '.jpg'
        cv2.imwrite(file_loc, img)
