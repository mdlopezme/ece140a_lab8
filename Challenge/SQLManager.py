from os import environ
from dotenv import load_dotenv
import mysql.connector as mysql
import numpy as np

class SQLManager():
    def __init__(self):
        # Load enviroment variables
        load_dotenv('credentials.env')
        db_host = environ['MYSQL_HOST']
        db_user = environ['MYSQL_USER']
        db_pass = environ['MYSQL_PASSWORD']
        db_name = environ['MYSQL_DATABASE']

        # Connect to database
        print('Opening Connection to database')
        self.db = mysql.connect(user=db_user,password=db_pass,host=db_host,db=db_name)
        self.cursor = self.db.cursor()

        self.__get_objects()
        self.set(self.objects[0]) # Set Default object

    def __get_objects(self):
        '''Returns a list of available objects'''
        try:
            self.cursor.execute('''
                SELECT type FROM Objects;
            ''')
        except:
            print('Unable to get objects from database')

        self.objects = np.array(self.cursor.fetchall())[:,0]

    def set(self, object):
        '''Give it a objectType'''
        # Get HSV VALUES
        try:
            self.cursor.execute(f'''
                SELECT lowH,lowS, lowV, higH,higS,higV FROM Objects WHERE type=\'{object}\';
            ''')
        except:
            print('Unable to get objects from database')
        
        values = np.array(self.cursor.fetchall())[0]

        # Set internal vars
        self.lower_hsv = values[0:3]
        self.upper_hsv = values[3:6]

    def add(self,object, coords):
        '''Give it an objectType and GPS Coordinates'''
        # Count number of object types
        try:
            self.cursor.execute(f'''
                SELECT COUNT(type) AS objectInstances from Found_Objects
                WHERE type=\'{object}\';
            ''')
        except:
            print('Unable to count object types in Found_Objects')

        num_of_objects = np.array(self.cursor.fetchall())[0,0]
        
        # Insert found object into database
        if num_of_objects == 0:
            self.cursor.execute(f'''
                INSERT INTO Found_Objects
                (name, address, type)
                VALUES
                (\'{object}\',\'{coords}\',\'{object}\')
            ''')
            self.db.commit()
        else:
            self.cursor.execute(f'''
                INSERT INTO Found_Objects
                (name, address, type)
                VALUES
                (\'{object+str(num_of_objects)}\',\'{coords}\',\'{object}\')
            ''')
            self.db.commit()
        
        print(f'New {object} found!')
    
    def __del__(self):
        print('Closing connection to database')
        self.db.close()

def main():
    sql = SQLManager()
    for object in sql.objects:
        sql.set(object)
        sql.add(object,'Some Coords hjgjhghj')

if __name__ == '__main__':
    main()

    
