import sys
import smbus2 as smbus
import time
import RPi.GPIO as GPIO
from smbus2 import i2c_msg

class I2C():
    def __init__(self,recieve_sig,eel):
        self.I2C_ADDR = 0x18
        self.receive_sig = recieve_sig 
        self.info = ["Name", "TempF", "Condi", "UVInd", "Humid", "CaloB", "StepC", "DistW", "Heart","Bright", "Temp", "Heart"]      # array with request strings
        if eel == None:
            self.eel = time
        else:
            self.eel = eel
        self.setup()

    def ConvertStringToBytes(self,src):
        converted = []
        for b in src:
            converted.append(ord(b))
        return converted

    def run(self):
        print("getting_data")
        data_array=[None]*(len(self.info)-1)        # Array that will store data to place into database
        with smbus.SMBus(1) as I2Cbus:
            for piece in range(len(self.info)):
                # Nano sends request string to ESP32
                BytesToSend = self.ConvertStringToBytes(self.info[piece])
                msg = i2c_msg.write(self.I2C_ADDR, BytesToSend)
                I2Cbus.i2c_rdwr(msg)
                self.eel.sleep(0.1)
                try:
                    # ESP32 responds with data from phone connection
                    msg = i2c_msg.read(self.I2C_ADDR, 32)
                    I2Cbus.i2c_rdwr(msg)
                    if piece ==0:
                        continue
                    data = list(msg)
                    length = (data.pop(0))
                    if length == 0:
                        data_array[piece-1]=None
                        continue
                    # Parse data into appropriate types
                    data = data[:length]
                    result_string = ''.join(chr(val) for val in data if val !=255)
                    if piece !=1 and piece !=3:
                        data_array[piece-1]=float(result_string)
                    else:
                        data_array[piece-1]=result_string
                    self.eel.sleep(0.1)
                except:
                    print("remote i/o error")
                    self.eel.sleep(0.1)
        return data_array                       # Return data to be stored into database

    def setup(self):
        GPIO.setup(self.receive_sig, GPIO.IN)   # Sets up recieve signal for data
        I2Cbus = smbus.SMBus(1)                 # Sets up I2C on I2C 1 of GPIO pinout
        

# if __name__ == '__main__':
#     setup()
