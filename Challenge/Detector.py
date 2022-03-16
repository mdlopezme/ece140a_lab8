import cv2 as cv
import numpy as np
from SQLManager import SQLManager
from queue import Queue
from threading import Thread

class Detector():
    def __init__(self, lower_hsv=[0,0,0], upper_hsv=[255,255,255]):
        # Set HSV Range
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        # Sequester the video capture device
        self.cap = cv.VideoCapture(0)
        # Set camera resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        # Good to initiliaze
        self.pv = 0.0
        self.detected = False

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam") 
    
    def update(self):
        '''Find centroid of the biggest surviving contour in a specified HSV range'''
        
        # Capture new image from source
        _, self.frame = self.cap.read()

        # convert to hsv colorspace
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(hsv, np.array(self.lower_hsv) , np.array(self.upper_hsv))

        # Opening operation on red_only for denoising
        self.mask=cv.morphologyEx(self.mask, cv.MORPH_OPEN, np.ones((5,5),np.uint8))

        # Find largest contour in intermediate image
        countours, _ = cv.findContours(self.mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        out = np.zeros(self.mask.shape, np.uint8)

        # Find the largest contour
        if len(countours):
            biggest_blob = max(countours, key=cv.contourArea)
            area = cv.contourArea(biggest_blob)
            if area > 50.0:
                cv.drawContours(out, [biggest_blob], -1, 255, cv.FILLED)
        
        # Keep only the biggest contour
        self.mask = cv.bitwise_and(self.mask, out)

        self.moment_search()

    def moment_search(self):
        '''calculate moments of binary image'''
        M = cv.moments(self.mask)

        if int(M["m00"]) != 0:
            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])

            # Convert to relative scale of (-1,1)
            _, w = np.shape(self.mask)
            self.pv = 2*(cX - w/2)/w

            # Object was detected
            self.detected = True
        else:
            self.detected = False

    def start(self,out_q):
        while True:
            self.update()
            out_q.put((self.detected,self.pv))

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()
        print(data)

def main():
    db = SQLManager()
    detector = Detector(db.lower_hsv,db.upper_hsv)
    q = Queue()
    # Set HSV range
    
    thread1 = Thread(target=detector.start, args=(q,))
    thread2 = Thread(target = consumer, args =(q, ))

    thread1.start()
    thread2.start()

if __name__ == '__main__':
    main()