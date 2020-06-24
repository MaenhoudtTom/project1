from RPi import GPIO
from smbus import SMBus
import time

class MPU6050:
    def __init__(self, address_mpu):
        self.address_mpu = address_mpu
        self.i2c = SMBus()
        self.setup()

    def setup(self):
        # open bus 1
        print('open bus 1')
        self.i2c.open(1)

        # sensor uit sleep modus halen
        print('sensor uit sleep modus halen')
        self.i2c.write_byte_data(self.address_mpu, 0x6B, 1)

        # instellen gyroscoop
        print('gyroscoop instellen')
        self.i2c.write_byte_data(self.address_mpu, 0x1B, 0x00)

    def read_data(self):
        # data inlezen
        raw_data = self.i2c.read_i2c_block_data(self.address_mpu, 0x43, 6)
        # gyro
        x_waarde_gyro = self.registerwaarden_omzetten(raw_data[0], raw_data[1])
        y_waarde_gyro = self.registerwaarden_omzetten(raw_data[2], raw_data[3])
        z_waarde_gyro = self.registerwaarden_omzetten(raw_data[4], raw_data[5])
        x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = self.omzetten_graden_per_seconde(x_waarde_gyro, y_waarde_gyro, z_waarde_gyro)

        return x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden

    @staticmethod
    def registerwaarden_omzetten(msb, lsb):
        msb = msb << 8

        if bin(msb)[2] == '1':
            msb = msb - 2**16
        
        waarde = msb | lsb
        waarde = waarde / 340 + 36.53

        return waarde

    @staticmethod
    def omzetten_graden_per_seconde(x_waarde, y_waarde, z_waarde):
        rot_x = x_waarde / 131
        rot_y = y_waarde / 131
        rot_z = z_waarde / 131
        
        return rot_x, rot_y, rot_z

    def opkuisen(self):
        self.i2c.close()

if __name__ == '__main__':
    try:
        mpu = MPU6050(0x68)
        while True:
            x_waarde_gyro_in_graden, y_waarde_gyro_in_graden, z_waarde_gyro_in_graden = mpu.read_data()
            print(f'rot_x: {round(x_waarde_gyro_in_graden, 2)}°/s | rot_y: {round(y_waarde_gyro_in_graden, 2)}°/s | rot_z: {round(z_waarde_gyro_in_graden, 2)}°/s')
            time.sleep(1)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        print('PI opkuisen')
        # mpu.opkuisen()