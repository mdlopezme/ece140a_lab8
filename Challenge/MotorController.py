from RpiMotorLib import RpiMotorLib
import cv2 as cv
from SQLManager import SQLManager
from Detector import Detector
from queue import Queue
from threading import Thread

class StepperMotor(RpiMotorLib.BYJMotor):
    def __init__(self,GpioPins = [18, 23, 24, 25]) -> None:
        super().__init__("MyMotorOne", "28BYJ")
        self.pins = GpioPins
        # Declare a named instance of class pass a name and motor type
        self.motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

    def update_speed(self,value):
        self.speed = (value - 100)/100.0

    def run(self,speed=0.0):
        '''The purpose of this method is to pass GPIO Pins to motor_run'''
        ccwise = speed < 0

        if speed == 0.0:
            super().motor_run(self.pins,0,0,ccwise,False,"full",.0)
        else:
            # Calculate wait
            wait = 0.02 - abs(speed)*(0.02 - 0.002)
            super().motor_run(self.pins,wait,1,ccwise,False,"half",.0)
    
    def start(self,in_q):
        while True:
            # Get some data
            [detected,pv] = in_q.get()
            if(detected):
                print(f'Process var: {pv}')
                self.run(pv)
            else:
                self.run()
                print('Not Found!')

def main():
    motor = StepperMotor()
    sql = SQLManager()
    detector = Detector(sql.lower_hsv,sql.upper_hsv)
    detection_queue = Queue()

    thread1 = Thread(target=detector.start, args=(detection_queue,))
    thread2 = Thread(target=motor.start, args =(detection_queue, ))

    thread1.start()
    thread2.start()

if __name__ == '__main__':
    main()
