#!/usr/bin/env python3
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from threading import Thread
from pyramid.response import FileResponse
from Detector import Detector
from queue import Queue
from SQLManager import SQLManager
from MotorController import StepperMotor
from GPS import GPS
import cv2 as cv
from time import sleep

class WebServer():
	def __init__(self):
		with Configurator() as config:
			# Add routes
			config.add_route('home','/')
			config.add_route('objects', '/objects')
			config.add_route('object_found', '/object_found')
			config.add_route('get_coords', '/get_coords')
			config.add_route('get_raw_coords', '/get_raw_coords')
			config.add_route('save_object', '/save_object')
			config.add_route('set_object', '/set_object')
			config.add_route('get_cam', '/get_cam')

			# Create views for routes
			config.add_view(self.get_home, route_name='home')
			config.add_view(self.get_objects, route_name='objects', renderer='json')
			config.add_view(self.object_found, route_name='object_found', renderer='json')
			config.add_view(self.get_coords, route_name='get_coords', renderer='json')
			config.add_view(self.get_raw_coords, route_name='get_raw_coords', renderer='json')
			config.add_view(self.save_object, route_name='save_object', renderer='json')
			config.add_view(self.set_object, route_name='set_object', renderer='json')
			config.add_view(self.get_cam, route_name='get_cam')

			# Static Routes
			config.add_static_view(name='/', path='WebServer:web_server/public/', cache_max_age=3600) # TODO: Relative path

			app = config.make_wsgi_app()

		self.server = make_server('0.0.0.0', 6543, app)

		self.start()

	def get_cam(self, req):
		smallImg = cv.resize(self.detector.frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
		cv.imwrite('temp.jpg', smallImg)
		return FileResponse('temp.jpg', request=req, content_type='image/jpeg' )

	def set_object(self, req):
		try:
			the_object=req.params['object']
			for object in self.sql.objects:
				if object == the_object:
					self.sql.set(object) # Fetch values from sql database
					self.detector.lower_hsv = self.sql.lower_hsv # Update detector values
					self.detector.upper_hsv = self.sql.upper_hsv # Update detector values
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
			coords = self.gps.loc # Get location String
			lat = coords[0]
			lon = coords[1]
			coords = str([lat, lon])
			self.sql.add(the_object,coords)
		except:
			return False
			
		return True

	def get_coords(self,req):
		return self.gps.loc

	def get_raw_coords(self,req):
		return self.gps.raw

	def object_found(self,req):
		return "True" if self.motor.object_found else "False"

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

	try:
		while True:
			sleep(100)
	except KeyboardInterrupt:
		server.stop()

if __name__ == '__main__':
	main()