import cv2
import imutils
import numpy as np
from datetime import datetime


class MotionDetection:
    def __init__(self, threshold=50, img_capture='image_captures/'):
        # threshold sets the min difference between the avg_img and the current frame
        self.threshold = threshold
        self.img_capture = img_capture
        self.avg_img = None

    def motion_detection(self, img):
        """
        Detects any motion in the frame
        :param img: current image being analyzed
        """
        if self.avg_img is None:
            self.avg_img = img #img.astype("float")

        # get any frame changes
        #cv2.accumulateWeighted(img, self.avg_img, 0.5)
        #diff_frames = cv2.absdiff(img, cv2.convertScaleAbs(self.avg_img))
        diff_frames = cv2.absdiff(img, self.avg_img)
        thresh_frames = cv2.threshold(diff_frames, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh_frames = cv2.dilate(thresh_frames, None, iterations=2)

        if not np.all(thresh_frames == 0):
            # get image contours
            self.motion_capture(img, thresh_frames)
            return True
        else:
            return False

    def motion_capture(self, img, thresh_frames):
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
                now = datetime.now()
                img_name = self.img_capture + now.strftime("%m-%d-%Y-%H:%M:%S") + '.jpg'
                cv2.imwrite(img_name, img)
