import threading
import cv2
from frame_analyzer import FrameAnalyzer
from video_frames import VideoFrames
from human_detection import HumanDetector


class SecuritySystem:
    def __init__(self, cam1_src=0, cam2_src=1, img_folder='image_captures/', threshold=0.7):
        # Load Human detection API
        self.human_detector = HumanDetector(threshold=threshold)

        # Start the cameras
        self.cam_1 = VideoFrames(cam1_src).start()
        self.cam_2 = VideoFrames(cam2_src).start()

        # Initialize frame analyzers
        self.analyzer_1 = FrameAnalyzer(cam_name="cam1", img_folder=img_folder, human_detector=self.human_detector)
        self.analyzer_2 = FrameAnalyzer(cam_name="cam2", img_folder=img_folder, human_detector=self.human_detector)

        self.stopped = False
        # Start surveillance system
        self.thread = threading.Thread(target=self.start_surveillance, args=()).start()

    def stop_surveillance(self):
        """
        Starts the surveillance system and human motion detection
        """
        self.cam_1.stop()
        self.cam_2.stop()
        self.stopped = True

    def start_surveillance(self):
        """
        Stops the surveillance system and human motion detection
        """
        while not self.stopped:
            # Camera frames
            frame1 = self.cam_1.frame
            frame2 = self.cam_2.frame

            # Analyze frames
            self.analyzer_1.motion_detection(frame1)
            self.analyzer_2.motion_detection(frame2)
