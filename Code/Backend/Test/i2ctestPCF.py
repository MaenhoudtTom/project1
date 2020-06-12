from RPi import GPIO
from smbus import SMBus
import time

def setup():
    GPIO.setmode(GPIO.BCM)

if __name__ == '__main__':
    try:
        setup()
        global pcf
        pcf = SMBus()
        pcf.open(1)
        while True:
            pcf.write_byte(0x20, 0xFF)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        pcf.close()