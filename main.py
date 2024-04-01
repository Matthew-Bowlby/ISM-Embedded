import eel
import RPi.GPIO as GPIO
motion_pin=12
eel.init("web")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motion_pin, GPIO.IN)

def screenControl():
    prev_val=None
    try:
        while True:

            val = GPIO.input(motion_pin)
            if val != prev_val:
                if val == GPIO.HIGH:
                    print("Motion detected!")
                    eel.wakeEvent()
                else:
                    eel.sleepEvent()

            prev_val=val
            eel.sleep(1)
    finally:
        GPIO.cleanup()
         

eel.spawn(screenControl)

eel.start("index.html", cmdline_args=["--kiosk"])

