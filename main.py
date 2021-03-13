import cv2

cam_1 = cv2.VideoCapture(0)
cam_2 = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret1, frame1 = cam_1.read()
    ret2, frame2 = cam_2.read()

    # Our operations on the frame come here
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame1',gray1)
    cv2.imshow('frame2', gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam_1.release()
cam_2.release()
cv2.destroyAllWindows()
