import time
import cv2
from motion_detection import MotionDetection
from video_frames import VideoFrames

# Start the cameras
cam_1 = VideoFrames(0).start()
cam_2 = VideoFrames(1).start()
time.sleep(3)

# Initialize motion detection
motion_1 = MotionDetection(cam_name="cam1", img_folder='image_captures/')
motion_2 = MotionDetection(cam_name="cam2", img_folder='image_captures/')


while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam_1.stop()
        cam_2.stop()
        break

    # Camera frames
    frame1 = cam_1.frame
    frame2 = cam_2.frame

    # Frame operations
    # Convert to grayscale
    gray_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Reduce image noise
    gray_1 = cv2.GaussianBlur(gray_1, (21, 21), 0)
    gray_2 = cv2.GaussianBlur(gray_2, (21, 21), 0)

    # Motion detection
    motion_1.motion_detection(gray_1)
    motion_2.motion_detection(gray_2)
