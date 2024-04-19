import sys
import smbus2 as smbus
import time
import RPi.GPIO as GPIO

I2C_ADDR = 0x18
receive_sig = 20 # change as needed
info = ["name", "indoor_tmp", "outdoor_tmp", "heartrate"]

def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def run():
    with smbus.SMBus(1) as I2Cbus:
        for piece in info:
            BytesToSend = ConvertStringToBytes(piece)
            print(BytesToSend)
            I2Cbus.write_i2c_block_data(I2C_ADDR, 0x00, BytesToSend)
            time.sleep(0.5)
            try:
                data = I2Cbus.read_i2c_block_data(I2C_ADDR, 0x20, 32)
                print("receive from slave:")
                print(data)
                # place data in database
                time.sleep(2.0)
            except:
                print("remote i/o error")
                time.sleep(2.0)

    return 0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(receive_sig, GPIO.IN)
    GPIO.add_event_detect(receive_sig, GPIO.rising, callback=run)
    I2Cbus = smbus.SMBus(1)
        

if __name__ == '__main__':
    setup()
