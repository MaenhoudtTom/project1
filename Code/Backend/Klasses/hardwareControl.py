# pylint: skip-file
from RPi import GPIO
import time
from subprocess import check_output

#import classes
from Klasses.Mcp import Mcp
from Klasses.PCF8574 import PCF8574
from Klasses.LCD_display import LCD_display
from Klasses.MPU6050 import MPU6050
from Klasses.ulstrasonic import Ultrasonic

class hardwareControl:
    def __init__(self):
        self.ldr = Mcp(0)
        self.ip_address = self.get_IP_address()
        self.setup()
        self.display = LCD_display(13, 19)
        self.mpu = MPU6050(0x68)
        self.ultra = Ultrasonic(25, 24)

    def setup(self):
        GPIO.setmode(GPIO.BCM)

    def read_ldr(self):
        value_ldr = self.ldr.read_channel(self.ldr.bus)
        return value_ldr

    def get_IP_address(self):
        ip = check_output(['hostname', '--all-ip-addresses'])
        ip = ip[:15].decode(encoding='utf8')
        return ip

    def show_ip_lcd(self):
        nieuw_ip_address = self.get_IP_address()
        if nieuw_ip_address != self.ip_address:
            self.display.send_instruction(1)
            self.display.write_message(nieuw_ip_address)
            self.ip_address = nieuw_ip_address
        time.sleep(60)

    def read_mpu(self):
        x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, temperatuur, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = self.mpu.read_data()
        return x_waarde_accelero_in_g, y_waarde_accelero_in_g, z_waarde_accelero_in_g, temperatuur, x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden

    def measure_distance(self):
        distance = self.ultra.measure_distance()

# if __name__ == '__main__':
#     try:
#         hardware = hardwareControl()
#         hardware.setup()
#         while True:
#             print(hardware.read_ldr())
#             hardware.angles()
#             time.sleep(1)
#     except KeyboardInterrupt as e:
#         print(e)
#     finally:
#         print("Cleaning up")
#         ldr.closespi()
#         GPIO.cleanup()