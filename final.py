from PIL import Image
#import pytesseract
import cv2 as cv
import threading
import os, sys, inspect
import imutils
from imutils.video import FPS
import time
import datetime
import numpy as np
from queue import Queue
import serial
import random

ser=serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
ser.reset_input_buffer()

class VideoCapture:
    
    def __init__(self, src=0):
        self.cap = cv.VideoCapture(0, cv.CAP_V4L2)

        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 320)
        self.cap.set(cv.CAP_PROP_FPS, 30)
        self.q = Queue(maxsize=128)
        self.stopped = False

    def start(self):
        thread = threading.Thread(target=self.update, daemon = True)
        thread.start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            ret, frame = self.cap.read()
            if not ret:
                self.stopped = True
                return
            
            if not self.q.full():
                self.q.put(frame)
            else:
                try:
                    self.q.get_nowait()
                except:
                    pass

    def read(self):
        return self.q.get()
    
    def stop(self):
        self.stopped = True





class VideoProcessor:
    def __init__(self, capture_source=0):
        self.capture = VideoCapture(capture_source).start()
        self.output_queue = Queue(maxsize=10)
        self.stopped = False

    def process_frame(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (5, 5), cv.BORDER_DEFAULT)
        ret, thresh = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)
        return thresh

    def start_processing(self):
        thread = threading.Thread(target=self._process_loop, daemon=True)
        thread.start()
        return self
    
    def _process_loop(self):
        while not self.stopped:
            frame = self.capture.read()
            processed = self.process_frame(frame)
            #print(frame.shape)

            if not self.output_queue.full():
                self.output_queue.put(processed)

    def read_processed(self):
        return self.output_queue.get()
    
    def stop(self):
        self.stopped = True
        self.capture.stop()

def main():
    processor = VideoProcessor(0).start_processing()
    fps_counter = 0
    fps_start_time = time.time()

    while True:
        ptD = [110, 140]
        ptC = [210, 140]
        ptA = [300, 320]
        ptB = [20, 320]
        width, height = 320, 320


        pts1 = np.float32([ptD, ptC, ptA, ptB])
        pts2 = np.float32([[0,0], [width, 0], [width, height], [0, height]])
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        try:
            processed_frame = processor.read_processed()
            
            fps_counter += 1
            if fps_counter %30 == 0:
                elapsed = time.time() - fps_start_time
                fps = fps_counter/elapsed
                print(f"Processing at {fps:.2f} FPS")
            canner = cv.Canny(processed_frame, 100, 200)
            contours, heirarchies = cv.findContours(canner, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            blank = np.zeros(processed_frame.shape[:2], dtype='uint8')
            cv.drawContours(blank, contours, -1, (255, 0, 0), 1)

            for i in contours:
                M = cv.moments(i)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    intccx = int(160-cx)
                    intccy = int(160-cy)
                    main.ccx = str(intccx)
                    main.ccy = str(intccy)
                    # int(320 - cx)
                    cv.drawContours(processed_frame, [i], -1, (255, 0, 0), 2)
                    cv.circle(processed_frame, (cx, cy), 7, (0, 0, 255), -1)
                    cv.putText(processed_frame, "center", (cx -20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    result = cv.warpPerspective(processed_frame, matrix, (width, height))
                    #print(f"x: {cx} y: {cy}")
                    cv.imshow("Contours", result)
            #cv.imshow('Perspective', result)
            #cv.imshow('Processed Feed', processed_frame)
            number = ser.write(main.ccx.encode('utf-8'))
            line= ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break
    processor.stop()
    cv.destroyAllWindows()
if __name__ == '__main__':
    main()
