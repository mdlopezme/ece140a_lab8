from time import sleep
from RpiMotorLib import RpiMotorLib
from SQLManager import SQLManager
from Detector import Detector
from queue import Queue
from threading import Thread
import cv2 as cv

class StepperMotor(RpiMotorLib.BYJMotor):
	def __init__(self, in_q, GpioPins = [18, 23, 24, 25]) -> None:
		print('Starting motor')
		super().__init__("MyMotorOne", "28BYJ")
		self.pins = GpioPins
		# Declare a named instance of class pass a name and motor type
		self.motor = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

		self.detecting = True
		self.tick = 0
		self.tot_ticks = 256
		self.search_direction = False

		# Start the thread
		thread = Thread(target=self.start, args=(in_q,))
		thread.start()

	def run(self,speed=0.0):
		'''The purpose of this method is to pass GPIO Pins to motor_run'''
		ccwise = speed < 0

		if abs(speed) < 0.15:
			super().motor_run(self.pins,0,0,ccwise,False,"full",.0)
		else:
			super().motor_run(self.pins,0.0025,1,ccwise,False,"half",.0)
			if ccwise:
				self.tick = self.tick - 1
			else:
				self.tick = self.tick + 1
			# print(self.tick)
	def search(self):
		if self.tick > self.tot_ticks: # Go the other way if limit reach
			self.run(-1.0)
			self.search_direction = True
		elif self.tick < -self.tot_ticks: # Go the other way if limit reach
			self.run(1.0)
			self.search_direction = False

		elif self.search_direction:
			self.run(-1.0)
		else:
			self.run(1.0)

	def start(self,in_q):
		# TODO: Include a way to keep track of the rotation
		while self.detecting:
			# Get some data
			[detected,pv] = in_q.get()
			if(detected):
				# print(f'Process var: {pv}')
				self.run(pv)
			else:
				self.search()
				# print('Not Found!')

	def stop(self):
		print('Stopping motor')
		self.detecting = False

def main():
	q = Queue(maxsize=1)
	sql = SQLManager()
	detector = Detector(q, sql.lower_hsv,sql.upper_hsv)
	motor = StepperMotor(q)
	
	# Show video feed
	try:
		while True:
			smallImg = cv.resize(detector.frame, None, fx=0.3, fy=0.3, interpolation=cv.INTER_AREA)
			cv.imshow('Webcam', smallImg)
			# Wait for q keypress or KeyboardInterrupt event to occur
			if cv.waitKey(1) & 0xFF == ord('q'):
				motor.stop()
				detector.stop()
				break
	except KeyboardInterrupt:
		motor.stop()
		detector.stop()

if __name__ == '__main__':
	main()
	print('done')
