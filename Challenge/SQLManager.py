class SQLManager():
    def __init__(self):
        # I'm setting some constants for now so I can work with the object detectionq
        # Set Color detection paramenters
        self.lower_hue1 = 0
        self.lower_sat1 = 144
        self.lower_val1 = 57
        self.upper_hue1 = 23
        self.upper_sat1 = 255
        self.upper_val1 = 185