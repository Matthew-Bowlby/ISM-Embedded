import sys
import smbus2 as smbus
import time
import RPi.GPIO as GPIO

class I2C():
    def __init__(self,recieve_sig,eel):
        self.I2C_ADDR = 0x18
        self.receive_sig = recieve_sig # change as needed
        self.info = ["name", "TempF", "Condi", "UVInd", "Humid", "CaloB", "StepC", "DistW", "Heart"]
        self.eel = eel
        self.setup()

    def ConvertStringToBytes(self,src):
        converted = []
        for b in src:
            converted.append(ord(b))
        return converted

    def run(self):
        data_array=[None]*len(self.info)
        with smbus.SMBus(1) as I2Cbus:
            for piece in range(len(self.info)):
                BytesToSend = self.ConvertStringToBytes(self.info[piece])
                print(BytesToSend)
                I2Cbus.write_i2c_block_data(self.I2C_ADDR, 0x00, BytesToSend)
                self.eel.sleep(0.5)
                try:
                    data = I2Cbus.read_i2c_block_data(self.I2C_ADDR, 0x20, 32)
                    print("receive from slave:")
                    print(data)
                    # place data in database
                    #data_array[piece]=data
                    self.eel.sleep(2.0)
                except:
                    print("remote i/o error")
                    self.eel.sleep(2.0)

        return data_array

    def setup(self):
        GPIO.setup(self.receive_sig, GPIO.IN)
        I2Cbus = smbus.SMBus(1)
        

# if __name__ == '__main__':
#     setup()
