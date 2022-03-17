from os import environ
from dotenv import load_dotenv
import mysql.connector as mysql

class SQLManager():
    def __init__(self):
        # I'm setting some constants for now so I can work with the object detectionq
        # Set Color detection paramenters
        self.lower_hsv = [0, 144, 57]
        self.upper_hsv = [23,255,185]

        # Load enviroment variables
        load_dotenv('credentials.env')
        db_host = environ['MYSQL_HOST']
        db_user = environ['MYSQL_USER']
        db_pass = environ['MYSQL_PASSWORD']

        # Connect to database
        print('Opening Connection to database')
        self.db = mysql.connect(user=db_user,password=db_pass,host=db_host)
        self.cursor = self.db.cursor()
    
    def __del__(self):
        print('Closing connection to database')
        self.db.close()

    
