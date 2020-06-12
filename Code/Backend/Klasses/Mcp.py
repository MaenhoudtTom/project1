# pylint: skip-file
from RPi import GPIO
import time
import spidev

class Mcp:
    def __init__(self, bus=0, device=0):
        self.bus = bus
        self.device = device
        self.startbyte = 1
        self.eindbyte = 0
        self.spi = spidev.SpiDev()
        GPIO.setmode(GPIO.BCM)

    def read_channel(self, channel):
        self.spi.open(0, 0)

        if channel == 0:
            commandobyte = 128 #kanaal 0
        elif channel == 1:
            commandobyte = 144 #kanaal 1

        bytes_out = [self.startbyte, commandobyte, self.eindbyte]
        self.spi.max_speed_hz = 10 ** 5
        bytes_in = self.spi.xfer(bytes_out)

        eerste_byte = bytes_in[1]
        tweede_byte = bytes_in[2]

        waarde = eerste_byte << 8 | tweede_byte

        return(waarde)

    def closespi(self):
        self.spi.close()

# pot_meter = Mcp(0)
# waarde_pot = pot_meter.read_channel(pot_meter.bus)
# print(f"waarde potentiometer: {waarde_pot}")
# pot_meter.closespi()

# phototrans = Mcp(1)
# waarde_phototrans = phototrans.read_channel(phototrans.bus)
# print(f"waarde phototransistor: {waarde_phototrans}")
# phototrans.closespi()