import threading
import time
import cv2
from motion_detection import MotionDetection
from video_frames import VideoFrames


class SecuritySystem:
    def __init__(self, cam1_src=0, cam2_src=1, img_folder='image_captures/'):
        # Start the cameras
        self.cam_1 = VideoFrames(cam1_src).start()
        self.cam_2 = VideoFrames(cam2_src).start()
        time.sleep(2)

        # Initialize motion detection
        self.motion_1 = MotionDetection(cam_name="cam1", img_folder=img_folder)
        self.motion_2 = MotionDetection(cam_name="cam2", img_folder=img_folder)

        self.stopped = False
        self.thread = threading.Thread(target=self.start_surveillance, args=()).start()

    def stop_surveillance(self):
        self.cam_1.stop()
        self.cam_2.stop()
        self.stopped = True

    def start_surveillance(self):
        while not self.stopped:
            # Camera frames
            frame1 = self.cam_1.frame
            frame2 = self.cam_2.frame

            # Frame operations
            # Convert to grayscale
            gray_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray_2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

            # Reduce image noise
            gray_1 = cv2.GaussianBlur(gray_1, (21, 21), 0)
            gray_2 = cv2.GaussianBlur(gray_2, (21, 21), 0)

            # Motion detection
            self.motion_1.motion_detection(gray_1)
            self.motion_2.motion_detection(gray_2)