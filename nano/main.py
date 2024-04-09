import eel
import RPi.GPIO as GPIO
import sys
import json
import numpy as np
from database import DB
light_pin = 32
motion_pin = 40
target_duty=0
duty = 0

eel.init("web")

login_status = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(light_pin, GPIO.OUT)

light_pwm = GPIO.PWM(light_pin, 150)


db = DB()

print("setup pins")


print("setup db")


def runFacialRecognition():
    global login_status
    # run facial rec and return user #
    user = 1
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
                    if not login_status:
                        print("Motion detected!")
                        eel.wakeEvent()
                        eel.spawn(turn_on)
                        #frControl = eel.spawn(runFacialRecognition)
                    else:
                        timeout_count = 0
                       
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
                        frControl.kill()

            prev_val = val
            eel.sleep(1)
    finally:
        GPIO.cleanup()

target_duty=DB.getUserVanity(0)
light_pwm.start(duty)
eel.spawn(screenControl)
print("starting")

eel.start("index.html", cmdline_args=["--kiosk"])
