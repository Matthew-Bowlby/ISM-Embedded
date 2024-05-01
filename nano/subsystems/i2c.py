import sys
import smbus2 as smbus
import time
import RPi.GPIO as GPIO
from smbus2 import i2c_msg

class I2C():
    def __init__(self,recieve_sig,eel):
        self.I2C_ADDR = 0x18
        self.receive_sig = recieve_sig # change as needed
        self.info = ["Name", "TempF", "Condi", "UVInd", "Humid", "CaloB", "StepC", "DistW", "Heart", "Heart"]
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
        data_array=[None]*(len(self.info)-1)
        with smbus.SMBus(1) as I2Cbus:
            for piece in range(len(self.info)):
                BytesToSend = self.ConvertStringToBytes(self.info[piece])
                #print(BytesToSend)
                msg = i2c_msg.write(self.I2C_ADDR, BytesToSend)
                I2Cbus.i2c_rdwr(msg)
                self.eel.sleep(0.1)
                #print("hello")
                try:
                    #data = I2Cbus.read_i2c_block_data(self.I2C_ADDR, 0x00, 32)
                    msg = i2c_msg.read(self.I2C_ADDR, 32)
                    I2Cbus.i2c_rdwr(msg)
                    if piece ==0:
                        continue
                    #print("receive from slave:")
                    #print(msg)
                    data = list(msg)
                    length = (data.pop(0))
                    if length == 0:
                        data_array[piece-1]=None
                        continue
                    data = data[:length]
                    print(data)
                    result_string = ''.join(chr(val) for val in data if val !=255)
                    #print(data)
                    '''
                    while data[0] == 238:
                        msg = i2c_msg.read(self.I2C_ADDR, 32)
                        I2Cbus.i2c_rdwr(msg)
                        print("receive from slave:")
                        print(msg)
                        data = list(msg)
                        '''
                    if piece !=1 and piece !=3:
                        data_array[piece-1]=float(result_string)
                    else:
                        data_array[piece-1]=result_string
                    # place data in database
                    #val=''.join(data).decode('utf-8')
                    #print(val)
                    #data_array[piece]=val
                    self.eel.sleep(0.1)
                except:
                    print("remote i/o error")
                    self.eel.sleep(0.1)
        print("done")
        return data_array

    def setup(self):
        GPIO.setup(self.receive_sig, GPIO.IN)
        I2Cbus = smbus.SMBus(1)
        

# if __name__ == '__main__':
#     setup()
