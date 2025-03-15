from gpiozero import LED, Button
from signal import pause
import sys
import time
import datetime
from send import P2P

P2Psend = P2P()
led = LED("BOARD11")
button = Button("BOARD13", pull_up=False)
sp=35

class GPIO():
    def __init__(self):
        self.button = 13
        self.led = 11
    def button(self):
        while True:
            if button.when_pressed == True:
                return 1
            else:
                return 0
    # def waitbutton(self):
    #     button.wait_for_press()
    def on():
            led.brink(on_time=0.5,off_time = 1,ackground = True )


    def off():
            led.off()
            button.wait_for_press
            # 無限ループ
            while True:
                # 主処理は何もしない
                time.sleep(1)

def button_callback(channel):
    button = 1

def button_pressed(gpio_no):
    button = 1

def off():
    motor.low()


def run(sec=0):
    motor.high()
    clock.sleep(sec)
    motor.low()
