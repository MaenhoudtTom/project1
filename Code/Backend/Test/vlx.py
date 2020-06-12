#py-lint: skip file
from RPi import GPIO
from smbus import SMBus
import time

class VL53LOX:
    def __init__(self, address):
        self.address = address
        self.i2c = SMBus()
        self.setup()

    def setup(self):
        self.i2c.open(1)

    def read_data(self):
        self.i2c.write_byte(self.address, 0)
        value = self.i2c.read_byte(self.address)
        return value

    def close(self):
        self.i2c.close()

if __name__ == '__main__':
    try:
        vl53 = VL53LOX(0x29)
        while True:
            value_vl53 = vl53.read_data()
            print(value_vl53)
            time.sleep(1)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        GPIO.cleanup()