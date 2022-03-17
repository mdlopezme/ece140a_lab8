from serial import Serial
from pynmea2 import parse
from reverse_geocoder import search
from threading import Thread

class GPS():
    def __init__(self) -> None:
        print('Starting GPS')
        self.device  = Serial("/dev/serial0")

        # Set starting loc
        self.get_coords()
        
        # Start Thread
        self.keepAlive = True
        thread = Thread(target=self.start)
        thread.start()

    def get_coords(self):
        '''Returns a coordinate tuple (lat,lon)'''

        # Get GPGGA Data
        data = (str)(self.device.readline())
        while data.find("$GPGGA,") <= 0:
            data = (str)(self.device.readline())

        # Convert GPGGA string to coordinates
        msg = parse(data[2:-5]) # Remove some weird characters
        coords = (msg.latitude,msg.longitude)
        
        # Reserve geocoding
        rg = search(coords)[0]

        city = rg['name']
        state = rg['admin1']
        county = rg['admin2']
        country = rg['cc']

        self.loc = city,county,state,country

    def start(self):
        while self.keepAlive:
            self.get_coords()

    def stop(self):
        print('Stoping GPS')
        self.keepAlive = False

def main():
    gps = GPS()
    while True:
        print(gps.loc)
        

if __name__ == '__main__':
    main()