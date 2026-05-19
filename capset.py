import cv2 as cv
import numpy as np
#cv.CAP_V4L2
vid = cv.VideoCapture(0, cv.CAP_V4L2)

vid.set(cv.CAP_PROP_FRAME_WIDTH, 320)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 180)
vid.set(cv.CAP_PROP_FPS, 30)

while True:
    print(vid.get(cv.CAP_PROP_FPS))
    print(vid.get(cv.CAP_PROP_FRAME_WIDTH))
    ret, frame = vid.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
    ret, thresh = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv.destroyAllWindows()
