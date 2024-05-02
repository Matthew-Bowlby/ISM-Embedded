import eel
import RPi.GPIO as GPIO
import sys
import json
import atexit
import numpy as np
from subsystems.database import DB
from subsystems.nfr6 import FaceRecognition
from subsystems.i2c import I2C
light_pin = 32
motion_pin = 40
recieve_sig=21
target_duty=0
duty = 0
active_user=None
disable_timeout = False
home = '/home/ism/ISM-Embedded/nano/'
eel.init(home+"web")

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
    global active_user
    #eel.sleep(30)
    print("running fr")
    user=fr.run_recognition()
    # run facial rec and return user #
    # user = 1
    if user != None:
        active_user=user
        userinfo,info=db.getUserData(user)
        light_pwm.ChangeDutyCycle(info["VANITY"])
        eel.loginEvent(userinfo)

        login_status = True



@eel.expose
def get_image():
    return fr.creatingImages()

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
    global active_user
    frControl = None
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
                            eel.spawn(turn_on)
                            frControl = eel.spawn(runFacialRecognition)
                            print("screenControl: starting recognition")                 
                        
                elif val == GPIO.LOW:
                    
                    timeout_count += 1
                    if login_status:
                        if timeout_count >= 60:
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

def createImages():
    eel.sleep(10)
    fr.startImageTaking()
    eel.startPicTaking()

@eel.expose
def stopCreating():
    print("stopped taking")
    global disable_timeout
    global active_user
    user=fr.stopCreating()
    disable_timeout=False

    active_user=user
    userinfo,_=db.getUserData(user)
        
    eel.loginEvent(userinfo)

    login_status = True

def updateBrightness(val):
    global target_duty
    target_duty=val
    if light_pwm.get_pwm_dutycycle() >0:
        light_pwm.ChangeDutyCycle(duty)
def updateValues(idc):
    data=i2c.run()
    global active_user
    global disable_timeout
    global db

    if not db.id_exists(data[0]):
        print(f"User: {data[0]} not found. Adding")
        db.addUser(data[0])
        disable_timeout=True
        fr.startImageTaking(data[0])
        eel.startPicTaking()
    db.updateUserData(data)

    if data[0]==active_user:
        usdata,_=db.getUserData(data[0])
        eel.updateEvent(usdata)
        updateBrightness(data[8])
def exit_handler():
    GPIO.cleanup()

if __name__ == "__main__":
    atexit.register(exit_handler)
    target_duty=float(db.getUserVanity("Default"))
    #light_pwm.start(duty)
    eel.spawn(screenControl)
    GPIO.add_event_detect(recieve_sig, GPIO.RISING, callback=updateValues)
    #eel.spawn(runFacialRecognition)
    #eel.spawn(createImages)
    print("starting")

    #eel.start("index.html")
    eel.start("index.html", cmdline_args=["--kiosk"])
