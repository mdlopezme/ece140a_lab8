import mysql.connector as mysql
import os
from dotenv import load_dotenv

################# WARNING ######################
'''
    THIS SCRIPT RESETS THE DATABASE
'''

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(user=db_user,password=db_pass,host=db_host)
cursor = db.cursor()

try:
    cursor.execute("DROP DATABASE Lab8;")
except:
    print('Database does not exist, creating..')

try:    
    cursor.execute("CREATE DATABASE Lab8;")
except:
    print('Critical Error')
    db.close()
    exit()

cursor.execute('Use Lab8;')

try:
    cursor.execute('''
        CREATE TABLE Objects(
            id          INT AUTO_INCREMENT PRIMARY KEY,
            type        VARCHAR(50) NOT NULL,
            lowH        INT NOT NULL,
            lowS        INT NOT NULL,
            lowV        INT NOT NULL,
            higH        INT NOT NULL,            
            higS        INT NOT NULL,
            higV        INT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Found_Objects(
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(50) NOT NULL,
            address     VARCHAR(50) NOT NULL,
            type        VARCHAR(50) NOT NULL
        )
    ''')
except:
    print('Was not able to create Tables')
    db.close()
    exit()

try:
    # Things to add
    type = ['pumpkin', 
            'calabaza', 
            'calavera']
    lower_hsv = [[0, 144, 57],
                [1,145,58],
                [2,146,59]]
    upper_hsv = [[23, 255, 185],
                [24,255,186],
                [25,255,187]]
    for i in range(0,3):
        cursor.execute(f'''
            INSERT INTO Objects
            (type, lowH, lowS, lowV, higH, higS, higV)
            VALUES
            (\'{type[i]}\', 
            {lower_hsv[i][0]}, {lower_hsv[i][1]}, {lower_hsv[i][2]},
            {upper_hsv[i][0]}, {upper_hsv[i][1]}, {upper_hsv[i][2]})
        ''')
        db.commit()
except:
    print('Failed')

db.close()