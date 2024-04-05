import eel
import RPi.GPIO as GPIO
import sqlite3
import sys
import json
import numpy as np

light_pin = 19
motion_pin = 12
current_duty=0
target_duty =0
eel.init("web")

login_status = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motion_pin, GPIO.IN)
GPIO.setup(light_pin, GPIO.OUT)

print("setup pins")

try:
    sqliteConnector = sqlite3.connect("user_data.db")
    cursor = sqliteConnector.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_data(
            NAME TEXT NOT NULL,
            TEMP REAL,
            VANITY INTEGER
                            

    );"""
    )
except sqlite3.Error as error:
    print(f"Error occured: {error}")
    sys.exit(1)
print("setup db")


def runFacialRecognition():
    global login_status
    name = "JP"
    cnt = cursor.execute(f"SELECT * from user_data WHERE NAME='{name}'")

    columns = [column[0] for column in cnt.description]
    out = cnt.fetchone()

    json_data = []
    row_data = {}
    for i in range(len(columns)):
        row_data[columns[i]] = out[i]
    json_data.append(row_data)
    json_output = json.dumps(json_data)
    eel.loginEvent(json_output)

    login_status = True


def turn_on():
    GPIO.output(light_pin, GPIO.HIGH)


def turn_off():
    GPIO.output(light_pin, GPIO.LOW)

def lightScale(dir):
    global target_duty
    global current_duty

    if dir:
        for x in np.linspace(current_duty, target_duty, 50, dtype=int):
            current_duty = x
    else:
        for x in np.linspace(target_duty, current_duty, 50, dtype=int):
            current_duty = x
def turnOnLights():
    global current_duty
    freq = 120  # for 120 hz
    current_duty = 0  # 1% of the period, the voltage must be high.

    period = 1 / freq

    # so the the duration for which the voltage will be high
    high_period = period * current_duty / 100  # percentange of period the signal is high
    low_period = period - high_period

    while True:
        try:
            turn_on()
            eel.sleep(high_period)
            turn_off()
            eel.sleep(low_period)
        except KeyboardInterrupt:
            break


def turnOffLights():
    freq = 120  # for 120 hz
    global current_duty

    period = 1 / freq

    # so the the duration for which the voltage will be high
    high_period = period * current_duty / 100  # percentange of period the signal is high
    low_period = period - high_period

    while current_duty>0:
        try:
            turn_on()
            eel.sleep(high_period)
            turn_off()
            eel.sleep(low_period)
        except KeyboardInterrupt:
            break
    turn_off()


def screenControl():
    global login_status
    lightControl=None
    frControl=None
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
                        lightControl= eel.spawn(turnOnLights)
                        frControl=eel.spawn(runFacialRecognition)
                    else:
                        timeout_count = 0

                else:
                    if not login_status:
                        eel.sleepEvent()
                        lightControl.kill()
                        frControl.kill()
                        eel.spawn(turnOffLights)
            elif val == GPIO.LOW:
                if login_status:
                    timeout_count += 1
                    if timeout_count == 60:
                        eel.sleepEvent()
                        login_status = False
                        timeout_count = 0
                        eel.spawn(turnOffLights)

            prev_val = val
            eel.sleep(1)
    finally:
        GPIO.cleanup()


eel.spawn(screenControl)
print("starting")

eel.start("index.html", cmdline_args=["--kiosk"])