# pylint: skip-file
from RPi import GPIO
import time

adres = 64

knop_verhogen = 19
knop_verlagen = 26

class PCF8574:
    def __init__(self, sda, scl, address):
        self.sda = sda
        self.scl = scl
        self.address = address
        self.delay = 0.002
        self.setup()
        self.startconditie()
        self.write_outputs(self.address)

    @property
    def address(self):
        """The address property."""
        return self._address
    @address.setter
    def address(self, value):
        self._address = value

    def write_outputs(self, data):
        # print(f"write outputs data {data}")
        #data wegschrijven
        self.writebyte(data)
        #ack
        self.ack()


    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sda, GPIO.OUT)
        GPIO.setup(self.scl, GPIO.OUT)
        GPIO.output(self.sda, GPIO.HIGH)
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)

    def startconditie(self):
        GPIO.output(self.sda, GPIO.LOW)
        time.sleep(self.delay)
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)

    def writebit(self, bit):
        GPIO.output(self.sda, bit)
        time.sleep(self.delay)
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)

    def writebyte(self, byte):
        mask = 0x80
        for i in range(8):
            self.writebit(byte & mask >> i)

    def stopconditie(self):
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        GPIO.output(self.sda, GPIO.HIGH)
        time.sleep(self.delay)

    def ack(self):
        GPIO.setup(self.sda, GPIO.IN, GPIO.PUD_UP)
        GPIO.output(self.scl, GPIO.HIGH)
        time.sleep(self.delay)
        waarde_sda = GPIO.input(self.sda)
        if waarde_sda != 0:
            print("Not OK")
        GPIO.setup(self.sda, GPIO.OUT)
        GPIO.output(self.scl, GPIO.LOW)
        time.sleep(self.delay)
    
    def shutdownpcf(self):
        GPIO.cleanup()

# if __name__ == "__main__":
#     try:
#         pcf = PCF8574(27, 22, adres)
#         pcf.setup()
#         #start
#         pcf.startconditie()
#         pcf.writebyte(pcf.address)
#         #ack
#         pcf.ack()
#         while True:
#             #data
#             segmenten = pcf.nummers[pcf._cijfer] | pcf.dot << 7
#             pcf.write_outputs(segmenten)
#             time.sleep(pcf.delay)
#     except KeyboardInterrupt as e:
#         print(e)
#     finally:
#         print("PI opkuisen")
#         #stop
#         pcf.stopconditie()
#         GPIO.cleanup()