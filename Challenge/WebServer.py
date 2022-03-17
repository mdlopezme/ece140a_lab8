#!/usr/bin/env python3
from http import server
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from threading import Thread
from pyramid.response import FileResponse
from Detector import Detector
from queue import Queue
from SQLManager import SQLManager
from MotorController import StepperMotor
from GPS import GPS
from time import sleep
import cv2 as cv
import numpy as np

class WebServer():
	def __init__(self):
		with Configurator() as config:
			# Add routes
			config.add_route('home','/')

			# Create views for routes
			config.add_view(self.get_home, route_name='home')

			app = config.make_wsgi_app()

		self.server = make_server('0.0.0.0', 6543, app)

		self.start()

	def get_home(self, req):
		return FileResponse('Challenge/web_server/index.html')

	def start(self):
		self.gps = GPS()
		self.q = Queue(maxsize=1)
		self.sql = SQLManager()
		self.detector = Detector(self.q, self.sql.lower_hsv,self.sql.upper_hsv)
		self.motor = StepperMotor(self.q)
		
		print('Web server started on: http://192.168.1.100:6543')
		self.server_thread = Thread(target=self.server.serve_forever,name="Web Server")
		self.server_thread.start()
	
	def stop(self):
		self.motor.stop()
		self.detector.stop()
		self.gps.stop()
		print("Ending webserver")
		self.server.shutdown()

def main():
	server = WebServer()

	# Show video feed
	while True:
		smallImg = cv.resize(server.detector.frame, None, fx=0.3, fy=0.3, interpolation=cv.INTER_AREA)
		cv.imshow('Webcam', smallImg)
		# Wait for q keypress or KeyboardInterrupt event to occur
		if cv.waitKey(1) & 0xFF == ord('q'):
			break

	server.stop()

if __name__ == '__main__':
	main()