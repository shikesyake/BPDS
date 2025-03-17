import gpiozero
import lgpio
from signal import pause
import sys
import time
import datetime
from send import P2P
##
p2p = P2P()
##led = LED("BOARD11")
##button = Button("BOARD13", pull_up=False)
##sp=35
##GPIOZERO_PIN_FACTORY=lgpio
##led = gpiozero.DigitalinputDevice(pin=27, pullup=True)
class GPIO():
    def __init__(self):
        self.button = gpiozero.Button(19, pull_up=True)
        self.led = gpiozero.LED(17)
        self.buz = gpiozero.Buzzer(27)
##    def button(self):
##        while True:
##            if self.button.is_pressed:
##                return 1
##            else:
##                return 0
    # def waitbutton(self):
    #     button.wait_for_press()
    def on(self, ):
        for i in range(5):
            self.led.blink(on_time=0.25,off_time = 0.25,background = True)
            self.buz.beep(on_time=0.20, off_time=0.20, background=True)
        self.button.wait_for_press()
        time.sleep(0.1)
        p2p.tomareya()
        self.led.off()
        self.buz.off()
##      self.led.on()
##      time.sleep(3)
##      self.led.off()
        #下直す
    def aawait(self):
        try:
            self.button.wait_for_press()
        finally:
            return value

    def off(self):
            self.led.off()
            self.buz.off()
            # 無限ループ
##            while True:
##                # 主処理は何もしない
##                time.sleep(1)

    def button_callback(channel):
        button = 1

    def button_pressed(gpio_no):
        button = 1


    def run(sec=0):
        motor.high()
        clock.sleep(sec)
        motor.low()
