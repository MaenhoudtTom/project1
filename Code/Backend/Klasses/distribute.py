# pylint: skip-file
from RPi import GPIO
import time

class Distribute:
    def __init__(self, stepper_pin_1, stepper_pin_2, stepper_pin_3, stepper_pin_4, dc_motor_1, dc_motor_2):
        self.stepper_pins = [stepper_pin_1, stepper_pin_2, stepper_pin_3, stepper_pin_4]
        self.dc_motor_1 = dc_motor_1
        self.dc_motor_2 = dc_motor_2
        self.steps = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        self.__setup()


    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.dc_motor_1, GPIO.OUT)
        GPIO.setup(self.dc_motor_2, GPIO.OUT)
        global motor_1
        global motor_2
        motor_1 = GPIO.PWM(self.dc_motor_1, 50)
        motor_2 = GPIO.PWM(self.dc_motor_2, 50)
        motor_1.start(0)
        motor_2.start(0)

    def __calculate_angles(self, player_amount):
        angle = round(512 / player_amount)
        print(angle)
        return angle


    def __doStep(self, angle):
        for i in range(angle):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.stepper_pins[pin], self.steps[halfstep][pin])
                time.sleep(0.001)
    
    def __shoot_card(self):
        motor_1.ChangeDutyCycle(50)
        motor_2.ChangeDutyCycle(50)
        time.sleep(0.5)
        motor_1.ChangeDutyCycle(0)
        motor_2.ChangeDutyCycle(0)

    def distribute_card(self, player_amount):
        angle = self.__calculate_angles(player_amount)
        self.__doStep(angle)
        # self.__shoot_card()


# if __name__ == '__main__':
#     try:
#         steppr = Distribute(12, 16, 20, 21)
#         steppr.distribute_card(6)
#     except KeyboardInterrupt as e:
#         print(e)
#     finally:
#         print("Cleaning up")
#         GPIO.cleanup()
