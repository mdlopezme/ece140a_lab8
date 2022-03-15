import RPi.GPIO as GPIO
import cv2 as cv

# import the library
from RpiMotorLib import RpiMotorLib

GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")


# call the function pass the parameters
cv.namedWindow('Controls')
# Create trackbars
cv.createTrackbar('Steps', 'Controls', 0, 255, update_steps)
cv.createTrackbar('Wait', 'Controls', 0, 255, update_wait)

#send 5 step signals 50 times in each direction.
for i in range(50):
    #           (pins, wait, steps, ccwise, verbose, steptype, initdelay)
    mymotortest.motor_run(GpioPins , .002, 5, False, False, "full", .05)
for i in range(50):
    mymotortest.motor_run(GpioPins , .002, 5, True, False, "full", .05)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()