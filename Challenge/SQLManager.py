class SQLManager():
    def __init__(self):
        # I'm setting some constants for now so I can work with the object detectionq
        # Set Color detection paramenters
        self.lower_hsv = [0, 144, 57]
        self.upper_hsv = [23,255,185]
