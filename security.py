from frame_analyzer import FrameAnalyzer
from human_detection import HumanDetector


class SecuritySystem:
    def __init__(self, img_folder='image_captures/', threshold=0.7):
        # Load Human detection API
        self.human_detector = HumanDetector(threshold=threshold)

        # Initialize frame analyzers
        self.analyzer1 = FrameAnalyzer(cam_name="cam1", img_folder=img_folder, human_detector=self.human_detector)
        self.analyzer2 = FrameAnalyzer(cam_name="cam2", img_folder=img_folder, human_detector=self.human_detector)

    def analyze_frames(self, img1, img2):
        frames = self.analyzer1.motion_detection(img1)
        frames2 = self.analyzer2.motion_detection(img2)
        return frames, frames2
