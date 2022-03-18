#!/usr/bin/env python3
from http import server
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from threading import Thread
from pyramid.response import FileResponse
from webob import Response
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
			config.add_route('objects', '/objects')
			config.add_route('object_found', '/object_found')
			config.add_route('get_coords', '/get_coords')
			config.add_route('save_object', '/save_object')
			config.add_route('set_object', '/set_object')

			# Create views for routes
			config.add_view(self.get_home, route_name='home')
			config.add_view(self.get_objects, route_name='objects', renderer='json')
			config.add_view(self.object_found, route_name='object_found', renderer='json')
			config.add_view(self.get_coords, route_name='get_coords', renderer='json')
			config.add_view(self.save_object, route_name='save_object', renderer='json')
			config.add_view(self.set_object, route_name='set_object', renderer='json')

			app = config.make_wsgi_app()

		self.server = make_server('0.0.0.0', 6543, app)

		self.start()

	def set_object(self, req):
		try:
			the_object=req.params['object']
			for object in self.sql.objects:
				if object == the_object:
					self.sql.set(object) # Fetch values from sql database
					self.detector.lower_hsv = self.sql.lower_hsv # Update detector values
					self.detector.upper_hsv = self.sql.upper_hsv # Update detector values
					print(self.detector.lower_hsv)
					return True
		except:
			return False
		
		return False # If for some reason, might as well have false

	def save_object(self, req):
		try:
			the_object=req.params['object']
			for object in self.sql.objects:
				if object == the_object:
					self.add_object(object)
					return True
		except:
			return False
		
		return False # If for some reason, might as well have false

	def add_object(self,the_object):
		try:
			coords = self.gps.loc
			lat = round(coords[0],5)
			lon = round(coords[1],5)
			coords = str([lat, lon])
			print(coords)
			self.sql.add(the_object,coords)
		except:
			return False

	def get_coords(self,req):
		return self.gps.loc

	def object_found(self,req):
		return self.motor.object_found

	def get_objects(self, req):
		ret = [o for o in self.sql.objects]
		ret.sort()
		return ret

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
	try:
		while True:
			smallImg = cv.resize(server.detector.frame, None, fx=0.3, fy=0.3, interpolation=cv.INTER_AREA)
			cv.imshow('Webcam', smallImg)
			# Wait for q keypress or KeyboardInterrupt event to occur
			if cv.waitKey(1) & 0xFF == ord('q'):
				server.stop()
				break
	except KeyboardInterrupt:
		server.stop()

if __name__ == '__main__':
	main()