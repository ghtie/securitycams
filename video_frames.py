from threading import Thread
import cv2


class VideoFrames:
    def __init__(self, src=0):
        self.cam = cv2.VideoCapture(src)
        self.ret, self.frame = self.cam.read()
        self.stopped = False

    def start(self):
        """
        Starts the main thread
        """
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """
        Gets the frames from the camera
        """
        while not self.stopped:
            if not self.ret:
                self.stop()
            else:
                self.ret, self.frame = self.cam.read()

    def stop(self):
        """
        Stops the main thread
        """
        self.stopped = True
