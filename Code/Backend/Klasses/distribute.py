# pylint: skip-file
from RPi import GPIO
import time


class Distribute:
    def __init__(self, stepper_pin_1, stepper_pin_2, stepper_pin_3, stepper_pin_4, dc_motor_1):
        self.stepper_pins = [stepper_pin_1,
            stepper_pin_2, stepper_pin_3, stepper_pin_4]
        self.dc_motor_1 = dc_motor_1
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

    def __calculate_angles(self, player_amount):
        angle = round(192 / player_amount)
        print(angle)
        return angle

    def __doStep(self, angle):
        for i in range(angle):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(
                        self.stepper_pins[pin], self.steps[halfstep][pin])
                time.sleep(0.001)

    def __return_step(self, angle):
        for i in range(angle):
            for halfstep in range(7, 0, -1):
                for pin in range(4):
                    GPIO.output(
                        self.stepper_pins[pin], self.steps[halfstep][pin])
                time.sleep(0.001)

    def __shoot_card(self):
        GPIO.output(self.dc_motor_1, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.dc_motor_1, GPIO.LOW)
        time.sleep(1.5)

    def distribute_card(self, player_amount, cards):
        angle = self.__calculate_angles(player_amount)
        self.__return_step(int(angle * (player_amount / 2)))
        for i in range(cards):
            for player in range(player_amount):
                self.__doStep(angle)
                self.__shoot_card()
                time.sleep(0.5)
                # return to start posistion for next round
            for player in range(player_amount):
                self.__return_step(angle)
        self.__doStep(int(angle * (player_amount / 2)))

    def remove_remaining_cards(self, player_amount, cards_per_player, card_decks):
        cards=card_decks * 52
        remaining_cards=cards - (player_amount * cards_per_player)
        for i in range(remaining_cards):
            self.__shoot_card()

if __name__ == '__main__':
    try:
        steppr=Distribute(12, 16, 20, 21, 18)
        steppr.distribute_card(3, 2)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        print("Cleaning up")
        GPIO.cleanup()
