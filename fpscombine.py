import cv2
import threading
from queue import Queue
import time

widj = 320
hgh = 240
class VideoCapture:
    
    def __init__(self, cv2.CAP_V4L2):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, widj)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hgh)
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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
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
        try:
            processed_frame = processor.read_processed()
            fps_counter += 1
            if fps_counter %30 == 0:
                elapsed = time.time() - fps_start_time
                fps = fps_counter/elapsed
                print(f"Processing at {fps:.2f} FPS")
            cv2.imshow('Processed Feed', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break
    processor.stop()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()
