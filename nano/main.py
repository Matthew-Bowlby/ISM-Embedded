import eel
import RPi.GPIO as GPIO
import sys
import json
import numpy as np
from subsystems.database import DB
from subsystems.nfr6 import FaceRecognition
from subsystems.i2c import I2C
light_pin = 32
motion_pin = 40
recieve_sig=20
target_duty=0
duty = 0

eel.init("web")

login_status = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.setup(recieve_sig, GPIO.IN)

light_pwm = GPIO.PWM(light_pin, 150)

fr = FaceRecognition()
db = DB()
i2c = I2C(recieve_sig,eel)
print("setup pins")


print("setup db")


def runFacialRecognition():
    global login_status
    eel.sleep(30)
    user=fr.run_recognition()
    # run facial rec and return user #
    # user = 1
    if user != None:
        userinfo=db.getUserData(1)
        
        eel.loginEvent(userinfo)

        login_status = True


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


def screenControl():
    global login_status
    lightControl = None
    frControl = None
    prev_val = None
    timeout_count = 0
    try:
        while True:

            val = GPIO.input(motion_pin)
            if val != prev_val:
                if val == GPIO.HIGH:
                    timeout_count = 0
                    if not login_status and frControl == None:
                        print("Motion detected!")
                        eel.wakeEvent()
                        eel.spawn(turn_on)
                        frControl = eel.spawn(runFacialRecognition)
                                         
                       
            elif val == GPIO.LOW:
                timeout_count += 1
                if login_status:
                    if timeout_count == 60:
                        eel.sleepEvent()
                        login_status = False
                        timeout_count = 0
                        eel.spawn(turn_off)
                else:
                    if timeout_count == 10:
                        eel.sleepEvent()
                        eel.spawn(turn_off)
                        if not frControl.dead:
                            fr.stop_recognition()

            prev_val = val
            eel.sleep(1)
    finally:
        GPIO.cleanup()


def updateValues():
    data=i2c.run()
    db.updateUserData(0,data[0],data[2],data[3])

target_duty=db.getUserVanity(0)
light_pwm.start(duty)
eel.spawn(screenControl)
GPIO.add_event_detect(recieve_sig, GPIO.rising, callback=updateValues)
#eel.spawn(runFacialRecognition)
print("starting")

eel.start("index.html", cmdline_args=["--kiosk"])
