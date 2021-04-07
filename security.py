import threading
import time
from frame_analyzer import FrameAnalyzer
from video_frames import VideoFrames
from human_detection import HumanDetector


class SecuritySystem:
    def __init__(self, cam1_src=0, cam2_src=1, img_folder='image_captures/', threshold=0.7):
        # Load Human detection API
        self.human_detector = HumanDetector('frozen_inference_graph.pb')
        self.threshold = threshold

        # Start the cameras
        self.cam_1 = VideoFrames(cam1_src).start()
        self.cam_2 = VideoFrames(cam2_src).start()
        time.sleep(2)

        # Initialize frame analyzers
        self.motion_1 = FrameAnalyzer(cam_name="cam1", img_folder=img_folder, model_threshold=threshold)
        self.motion_2 = FrameAnalyzer(cam_name="cam2", img_folder=img_folder, model_threshold=threshold)

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

            # Analyze frames
            self.motion_1.motion_detection(frame1)
            self.motion_2.motion_detection(frame2)
