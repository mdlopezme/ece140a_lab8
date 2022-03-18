# Lab 8
## Information
Olivier Rogers: A16069362  
Moises Lopez: A14156109
## Introduction


## Tutorials

### Tutorial 1: Introduction to CAD

In this tutorial we used Solidworks to make the part especified in the tutorial.  
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