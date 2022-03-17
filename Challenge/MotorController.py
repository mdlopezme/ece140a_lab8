from time import sleep
from RpiMotorLib import RpiMotorLib
from SQLManager import SQLManager
from Detector import Detector
from queue import Queue
from threading import Thread

class StepperMotor(RpiMotorLib.BYJMotor):
    def __init__(self, in_q, GpioPins = [18, 23, 24, 25]) -> None:
        super().__init__("MyMotorOne", "28BYJ")
        self.pins = GpioPins
        # Declare a named instance of class pass a name and motor type
        self.motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

        self.detecting = True
        self.tick = 0
        self.tot_ticks = 1024

        # Start the thread
        thread = Thread(target=self.start, args=(in_q,))
        thread.start()

    def run(self,speed=0.0):
        '''The purpose of this method is to pass GPIO Pins to motor_run'''
        ccwise = speed < 0
        sum = 

        if abs(speed) < 0.15:
            super().motor_run(self.pins,0,0,ccwise,False,"full",.0)
        else:
            super().motor_run(self.pins,0.0025,1,ccwise,False,"half",.0)

    def start(self,in_q):
        # TODO: Include a way to keep track of the rotation
        while self.detecting:
            # Get some data
            [detected,pv] = in_q.get()
            if(detected):
                print(f'Process var: {pv}')
                self.run(pv)
            else:
                self.run()
                print('Not Found!')

    def stop(self):
        print('stop motor')
        self.detecting = False

def main():
    try:
        q = Queue(maxsize=1)
        sql = SQLManager()
        detector = Detector(q, sql.lower_hsv,sql.upper_hsv)
        motor = StepperMotor(q)

        while True:
            sleep(1)
    except KeyboardInterrupt:
        print('Hi')
        motor.stop()
        detector.stop()
    print('done')

if __name__ == '__main__':
    main()
