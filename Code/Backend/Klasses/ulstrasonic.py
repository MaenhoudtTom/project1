#pylint: skip-file
from RPi import GPIO
import time

class Ultrasonic:
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trigger, GPIO.OUT)

    def measure_distance(self):
        GPIO.output(self.trigger, 1)
        time.sleep(0.00001)
        GPIO.output(self.trigger, 0)

        start_time = time.time()
        stop_time = time.time()

        # save start_time
        while GPIO.input(self.echo) == 0:
            start_time = time.time()

        # save time of arrival (stop_time)
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()

        time_difference = stop_time - start_time
        #multiply with the sonic speed (34300 cm/s)
        #divide by 2, go and back
        distance = time_difference * 34300 / 2

        return distance

# if __name__ == '__main__':
#     try:
#         ultra = Ultrasonic(25, 24)
#         while True:
#             distance = ultra.measure_distance()
#             print(distance)
#             time.sleep(1)
#     except KeyboardInterrupt as e:
#         print(e)
#     finally:
#         GPIO.cleanup()