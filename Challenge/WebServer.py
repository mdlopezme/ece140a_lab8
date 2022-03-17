#!/usr/bin/env python3
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from threading import Thread
from pyramid.response import FileResponse
from Detector import Detector
from queue import Queue
from SQLManager import SQLManager
from MotorController import StepperMotor
from time import sleep

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
        print('Web server started on: http://192.168.1.100:6543')
        self.server_thread = Thread(target=self.server.serve_forever,name="Web Server")
        self.server_thread.start()
    
    def __del__(self):
        print("Ending webserver")
        self.server.shutdown()

def main():
    try:
        q = Queue(maxsize=1)
        sql = SQLManager()
        detector = Detector(q, sql.lower_hsv,sql.upper_hsv)
        motor = StepperMotor(q)
        server = WebServer()

        while True:
            sleep(1)
    except KeyboardInterrupt:
        motor.stop()
        detector.stop()

if __name__ == '__main__':
    main()