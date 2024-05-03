#!/usr/bin/python3

# Import necessary modules
import eel
import RPi.GPIO as GPIO
import sys
import json
import atexit
import numpy as np
from subsystems.database import DB
from subsystems.nfr6 import FaceRecognition
from subsystems.i2c import I2C

# Define GPIO pins
light_pin = 32
motion_pin = 40
recieve_sig=21

# Initialize PWM variables
target_duty=0
duty = 0

# Initialize variables for user and timeout control
active_user=None
disable_timeout = False
login_status = False

# Set home directory for files
home = '/home/ism/ISM-Embedded/nano/'

# Initialize Eel
eel.init(home+"web")


# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.setup(recieve_sig, GPIO.IN)

# Initialize PWM for light control
light_pwm = GPIO.PWM(light_pin, 150)
light_pwm.start(0)

# Initialize Face Recognition, Database, and I2C classes
fr = FaceRecognition()
db = DB()
i2c = I2C(recieve_sig,eel)

# Function to run facial recognition process
def runFacialRecognition():
    global login_status
    global active_user
    print("running fr")
    user=fr.run_recognition()
    if user != None:
        active_user=user
        userinfo,info=db.getUserData(user)
        if info["VANITY"] is not None:
            light_pwm.ChangeDutyCycle(info["VANITY"]) # set vanity strength to user's preference
        eel.loginEvent(userinfo)

        login_status = True


# Function to get camera image
@eel.expose
def get_image():
    return fr.creatingImages()

# Functions to smoothly control light brightness 
def turn_on():
    global duty
    global target_duty
    while duty<target_duty:
        duty += 1
        light_pwm.ChangeDutyCycle(duty)
        eel.sleep(0.01)


def turn_off():
    global duty
    global target_duty
    while duty>0:
        duty -= 1
        light_pwm.ChangeDutyCycle(duty)
        eel.sleep(0.01)

# Function to control screen and timeout
def screenControl():
    global login_status
    global active_user
    global disable_timeout
    prev_val = None

    timeout_count = 0
    try:
        while True:
            if not disable_timeout:
                val = GPIO.input(motion_pin)
                if val != prev_val:
                    print(val)
                    if val == GPIO.HIGH:
                        timeout_count = 0
                        if not login_status:# and frControl == None:
                            print("Motion detected!")
                            eel.wakeEvent()
                            turn_on()
                            frControl = eel.spawn(runFacialRecognition)
                            print("screenControl: starting recognition")                 
                        
                elif val == GPIO.LOW:
                    
                    timeout_count += 1
                    if login_status:
                        if timeout_count >= 30:
                            eel.sleepEvent()
                            login_status = False
                            active_user= None
                            timeout_count = 0
                            eel.spawn(turn_off)
                    else:
                        print(timeout_count)
                        if timeout_count >= 10:
                            eel.sleepEvent()
                            eel.spawn(turn_off)
                            fr.stop_recognition()

                prev_val = val
            eel.sleep(1)
    finally:
        GPIO.cleanup()

# Function to stop creating images
@eel.expose
def stopCreating():
    print("stopped taking")
    global disable_timeout
    global active_user
    user=fr.stopCreating()
    fr.load_face()
    disable_timeout=False

    active_user=user
    userinfo,_=db.getUserData(user)
        
    eel.loginEvent(userinfo)

    login_status = True

# Function to update user values
def updateValues(idc):
    data=i2c.run()
    global active_user
    global disable_timeout
    global db
    # adds user if they dint exist and begin profile creation process
    if not db.id_exists(data[0]):
        print(f"User: {data[0]} not found. Adding")
        db.addUser(data[0])
        disable_timeout=True
        fr.stop_recognition()
        fr.startImageTaking(data[0])
        eel.startPicTaking()
    db.updateUserData(data) #stores user data

    #Updates user infomation live if they ar logged in
    if data[0]==active_user:
        usdata,info=db.getUserData(data[0])
        eel.updateEvent(usdata) 
        if info["VANITY"] is not None:
            light_pwm.ChangeDutyCycle(info["VANITY"])

def exit_handler():
    GPIO.cleanup()



if __name__ == "__main__":
    atexit.register(exit_handler)
    target_duty=float(db.getUserVanity("Default"))
    
    # start screen control thread
    eel.spawn(screenControl)

    # start i2c data handling thread if recieved a signal to request for data
    GPIO.add_event_detect(recieve_sig, GPIO.RISING, callback=updateValues)
    print("starting")

    # starting program
    eel.start("index.html", cmdline_args=["--kiosk"])
