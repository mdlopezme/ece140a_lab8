# Lab 8
## Information
Olivier Rogers: A16069362  
Moises Lopez: A14156109
## Introduction


## Challenge: The Final Boss

### Programming
All of the following modules work on their own thread. So that ther internal internal variables are always up to date.

### Detector.py
This module does the following.
- Gets image from the camera.
- Converts RGB to HSV color space
- Selects HSV range based on values sent HSV values from SQLManager.
- Does some more processing to select the biggest object of the given HSV range in the image.
- Finds the horizontal offset to be sent to the MotorController

### GPS.py
This module does the following.
- Retrives the GPGGA coordinates from the device
- Converts the GPGGA coordinates to latitude and longtitude in degrees
- Then the degress are passed to a reversed geocoding library

The program will store the values listed above to be retrieved later by the webserver.
### MotorController.py
The motor controller uses the values sent from the detector to actuate the stepper motor.
If no centroid is sent, that means the camera cannot see any object. So the motorcontroller sets the state of searching for the object. It does this by panning around until an object is found.

### SQLManager.py
The purpose of this module is to control the comunication to the SQL database. This module keeps the values lower_hsv and upper_hsv that the detector needs.

For example. To set the hsv_values to pumpkin. We need to initialize an instance, Return a list of objects available in the database.
```
sql = SQLManager()
objects = sql.objects
```

Then use this list to choose any of the available objects to track.
If we do.
```
sql.set(object)
```
The sql will take care of the rest to get the values back from the database and send the hsv range values to the detector.

### WebServer.py
The webserver incorporates all of the afore mentioned modules. The ultimate goal of the webserver is to connect all the modules to serve an API. That can tell a web browser if the ball is seen, select the object that the detector is looking for, summit an object to be added to the database, amount many more things.


## Tutorials

### Tutorial 1: Introduction to CAD

In this tutorial we used Solidworks to make the part especified in the t
torial.  
Then exported it to STL, and ended up printing it in the ECE Makerspace.
![Motor Mount CAD](Images/motor_mount.png)

### Tutorial 2: Welcome to GPS
In this tutorial we learned how to connect a gps module to the Raspberry. And use Python to print the '$GPGGA' string from the device.


### Tutorial 3: Color Segmentation

This tutorial showed how to track an object by color. This was done by creating a mask that selects color values within a certain range, denoising, connecting adjacent masked values into objects, and selecting the largest object. Using the HSV color space allows good color tracking with good tolerance for poor lighting.    

### Tutorial 4: Steper Motor
This tutorial showed the steper motor's internal workings. The device uses a rotor that creates magnetic fields by energising an eletromagnet. Then there is a responsive motor that has permanent magnet that align to the electromagnet's magnetic fields. We learned that the motor can do 360/(64*64) degree turn. And lastly learned how to control the device using python scripts.

![segmentation](Images/tutorial2_segmentation.gif)  
*Live feed of selected mask next to input image.*

### Tutorial 5: PID Controller
In this tutorial we learn how a PID feedback loop works. And how to implement PID in python.