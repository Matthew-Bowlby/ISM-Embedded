# ISM-Embedded
ISM embedded codebase

This codebase contains two main folders: nano and server_code

## nano

- The nano folder has a `main.py` file, `requirements.txt` file, `unlock.txt` file, `subsystems` folder, `web` folder, and `models` folder. 
  - `requirements.txt` includes the Python libraries needed for the project. 
  - `unlock.txt` contains commands that are needed to unlock the PWM on the Nano. 
  - `main.py` integrates the control for the display, facial recognition, I2C, database, and LED control.
- The `subsystems` folder contains files for facial recognition, I2C, and database.  These files describe the functionality of each module that is integrated into `main.py`.
- The `web` folder contains all of the code for the display control.
- The `models` folder contains the facial recognition models required.

## server_code

- The server_code is the folder containing the code for the ESP32. 
  - It has a `platformio.ini` file such that uploading to the ESP32 is simple for the user.  
  - The `include` folder contains an AES and JSON library that is used in the main file. 
  - Within the `src` folder contains the description for the AES algorithm and the `main.cpp` file.
- The `main.cpp` file contains all the controls for the ESP32. 
  - This file contains code to connect to the corresponding app over BLE. 
  - It will receive data over BLE and store it into a JSON to prepare for sending over I2C to the nano. 
  - It also has GPIO connections to sensors that will signal the nano for facial recognition. 
