import time
import cv2
from motion_detection import MotionDetection


# Start the cameras
cam_1 = cv2.VideoCapture(0)
cam_2 = cv2.VideoCapture(1)
time.sleep(3)

# Initialize motion detection
motion_1 = MotionDetection(img_capture='image_captures/cam1/')
motion_2 = MotionDetection(img_capture='image_captures/cam2/')

while True:
    # Camera frames
    ret_1, frame1 = cam_1.read()
    ret_2, frame2 = cam_2.read()

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

    # Display the camera feeds
    cv2.imshow('Camera Feed 1', gray_1)
    cv2.imshow('Camera Feed 2', gray_2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam_1.release()
cam_2.release()
cv2.destroyAllWindows()
