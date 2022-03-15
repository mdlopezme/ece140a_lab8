import cv2 as cv
import numpy as np
from SQLManager import SQLManager as sql

class DetectCircle(sql):
    def __init__(self):
        # Inherit parent properties
        super().__init__()

        # Sequester the video capture device
        self.cap = cv.VideoCapture(0)
        # Set camera resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam") 
    
    def hsv_search(self):
        '''Find centroid of the biggest surviving contour in a specified HSV range'''
        
        # Capture new image from source
        _, self.frame = self.cap.read()

        # convert to hsv colorspace
        hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(hsv, np.array([self.lower_hue1,self.lower_sat1,self.lower_val1]) , 
            np.array([self.upper_hue1, self.upper_sat1, self.upper_val1]))

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
            cY = int(M["m01"] / M["m00"])

            h, w = np.shape(self.mask)
            relX = (cX - w/2)/w
            relY = (h-cY)/h

            print((int(relX*100),int(relY*100)))

def main():
    detector = DetectCircle()
    
    while True:
        detector.hsv_search()
        # Wait for q keypress or KeyboardInterrupt event to occur
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()