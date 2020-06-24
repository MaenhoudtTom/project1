# pylint: skip-file
from RPi import GPIO
from .PCF8574 import PCF8574
import time


class LCD_display:
    def __init__(self,rs, enable, delay=0.01):
        self.rs = rs
        self.enable = enable
        self.small_delay = delay
        self.setup()
        self.init_LCD()

    global pcf
    pcf = PCF8574(17, 27, 0x70)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)

    def set_data_bits(self, value):
        pcf.write_outputs(value)

    def send_instruction(self, value):
        GPIO.output(self.rs, GPIO.LOW)
        GPIO.output(self.enable, GPIO.HIGH)
        self.set_data_bits(value)
        GPIO.output(self.enable, GPIO.LOW)
        time.sleep(self.small_delay)

    def send_character(self, value):
        ascii_waarde = ord(value)
        GPIO.output(self.rs, GPIO.HIGH)
        GPIO.output(self.enable, GPIO.HIGH)
        self.set_data_bits(ascii_waarde)
        GPIO.output(self.enable, GPIO.LOW)
        time.sleep(self.small_delay)

    def init_LCD(self, cursor=0, blinken=0):
        #function set
        print("------------------------")
        print("function set")
        self.send_instruction(56)
        #display on
        print("------------------------")
        print("display on")
        self.send_instruction(12 | (cursor << 1) | blinken)
        #clear display en cursor home
        print("------------------------")
        print("clear display and cursor home")
        self.send_instruction(1)
        print("------------------------")

    def write_message(self, message):
        index_char = 0
        for char in message:
            #print(char)
            if index_char == 23: #23 eerste teken dat buiten beeld valt geheugencel 17
                self.send_instruction(0x40 | 128) #128 voor d7
                self.send_character(char)
            else:
                self.send_character(char)
                index_char += 1

        if len(message) > 32:
            self.send_instruction(24)
            time.sleep(5)

    def shutdownlcd(self):
        pcf.shutdownpcf()

# if __name__ == "__main__":
#     try:
#         display = LCD_display(13, 19)
#         display.setup()
#         display.init_LCD()
#         while True:
#             print("Wat wilt u doen: cursor opties: [C], bericht sturen: [B]")
#             keuze = input("Uw keuze: ")
#             if keuze.upper() == "C":
#                 print("Cursor aan of uit? [aan, uit]")
#                 optie_cursor = input("Uw keuze: ")
#                 print("Blinken cursor aan of uit? [aan, uit]")
#                 optie_blinken = input("Uw keuze: ")
#                 if optie_cursor.upper() == "AAN":
#                     optie_cursor = 1
#                 elif optie_cursor.upper() == "UIT":
#                     optie_cursor = 0
#                 else:
#                     print("U gaf geen geldige keuze op voor de cursor. Cursor is uitgeschakeld.")
#                     optie_cursor = 0

#                 if optie_blinken.upper() == "AAN":
#                     optie_blinken = 1
#                 elif optie_blinken.upper() == "UIT":
#                     optie_blinken = 0
#                 else:
#                     print("U gaf geen geldige keuze op voor de blinkfunctie. Blinkfunctie is uitgeschakeld.")
#                     optie_blinken = 0

#                 display.init_LCD(optie_cursor, optie_blinken)
#             elif keuze.upper() == "B":
#                 message = input("Geef de boodschap die u wilt schrijven naar het diplay: ")
#                 display.send_instruction(1)
#                 display.write_message(message)
#             else:
#                 print("Gelieve een geldige keuze in te geven.")
#     except KeyboardInterrupt as e:
#         print(e)
#     finally:
#         print("Programma afgesloten.")