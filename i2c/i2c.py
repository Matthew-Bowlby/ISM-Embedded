import sys
import smbus2 as smbus
import time

I2C_ADDR = 0x18

def ConvertStringToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def main():
    I2Cbus = smbus.SMBus(1)
    with smbus.SMBus(1) as I2Cbus:
        BytesToSend = ConvertStringToBytes("hello")
        print(BytesToSend)
        I2Cbus.write_i2c_block_data(I2C_ADDR, 0x00, BytesToSend)
        time.sleep(0.5)
    
        while True:
            try:
                data = I2Cbus.read_i2c_block_data(I2C_ADDR, 0x20, 32)
                print("receive from slave:")
                print(data)
                time.sleep(2.0)
            except:
                print("remote i/o error")
                time.sleep(2.0)
    return 0
        


if __name__ == '__main__':
    main()
