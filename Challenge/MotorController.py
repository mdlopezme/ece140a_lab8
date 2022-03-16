from RpiMotorLib import RpiMotorLib

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

def main():
    motor = StepperMotor()

    while True:
        for i in range(-100,100):
            motor.run(i/100.0)

    # motor.__del__()

if __name__ == '__main__':
    main()
