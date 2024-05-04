# ISM-Embedded
ISM embedded codebase

This codebase contains two main folders: nano and server_code

## nano

- The nano folder has a main.py file, requirements file, unlock file, subsystems folder, web folder, and models folder. 
 - The requirements file includes the python libraries needed for the project. 
 - The unlock file is commands that are needed to unlock the pwm on the Nano. 
 - The main.py file which integrates the control for the display, facial recognition, i2c, database, and LED control.
- The subsystems folder contains files for the facial recognition, i2c, and database.  These files describe the functionality of each module that is integrated into main.py
- The web folder contains all of the code for the display control.
- The models folder contains the facial recognition models required.

## server_code

- The server_code is the folder containing the code for the ESP32. It has a platformio file such that uploading to the ESP32 is simple for the user.  The include folder contains an aes and json library that is used in the main file. Within the src folder contains the description for the aes algorithm and the main.cpp file.
- The main.cpp file contains all the controls for the ESP32. This file contains code to connect to the corresponding app over BLE. It will recieve data over BLE, store it into a json to prepare for sending over i2c to the nano. It also has GPIO connections to sensors that will signal the nano for facial recognition. 
