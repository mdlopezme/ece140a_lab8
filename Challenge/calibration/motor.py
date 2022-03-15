import RPi.GPIO as GPIO
import cv2 as cv
# import the library
from RpiMotorLib import RpiMotorLib

class StepperMotor(RpiMotorLib.BYJMotor):
    def __init__(self,GpioPins = [18, 23, 24, 25]) -> None:
        super().__init__("MyMotorOne", "28BYJ")
        self.pins = GpioPins
        # Declare a named instance of class pass a name and motor type
        self.motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

    def create_controls(self):
        # call the function pass the parameters
        cv.namedWindow('Controls')
        # Create trackbars
        cv.createTrackbar('Steps', 'Controls', 0, 255, self.update_steps)
        cv.createTrackbar('Wait', 'Controls', 0, 255, self.update_wait)

    def run(self, wait, steps, ccwise):
        super().motor_run(self.pins,wait,steps,ccwise,False,"full",.05)

    def __del__(self):
        GPIO.cleanup()

def main():
    motor = StepperMotor()
    #send 5 step signals 50 times in each direction.
    for i in range(50):
        #           (pins, wait, steps, ccwise, verbose, steptype, initdelay)
        motor.run(0.002,5,False)
    for i in range(50):
        motor.run(0.002,5,True)

if __name__ == '__main__':
    main()
