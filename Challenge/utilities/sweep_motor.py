import cv2 as cv
from RpiMotorLib import RpiMotorLib
import threading

class StepperMotor(RpiMotorLib.BYJMotor):
    def __init__(self,GpioPins = [18, 23, 24, 25]) -> None:
        super().__init__("MyMotorOne", "28BYJ")
        self.pins = GpioPins
        # Declare a named instance of class pass a name and motor type
        self.motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
        self.cap = cv.VideoCapture(0)
        # Set camera resolution
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640/2)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480/2)

    def __del__(self):
        # GPIO clean up is ran automatically on program exit
        # GPIO.cleanup()
        pass

    def create_controls(self):
        # call the function pass the parameters
        cv.namedWindow('Controls')
        # Create trackbars
        cv.createTrackbar('Speed', 'Controls', 100, 200, self.update_speed)

    def update_speed(self,value):
        self.speed = (value - 100)/100.0

    def run(self):
        '''The purpose of this method is to pass GPIO Pins to motor_run'''
        _, self.frame = self.cap.read()
        cv.imshow('Controls', self.frame)

        ccwise = self.speed < 0

        if self.speed == 0.0:
            super().motor_run(self.pins,0,0,ccwise,False,"full",.0)
        else:
            # Calculate wait
            wait = 0.02 - abs(self.speed)*(0.02 - 0.002)
            super().motor_run(self.pins,wait,1,ccwise,False,"half",.0)

def main():
    motor = StepperMotor()
    motor.create_controls()
    while True:
        motor.run()
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # motor.__del__()

if __name__ == '__main__':
    main()
