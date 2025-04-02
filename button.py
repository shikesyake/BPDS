import gpiozero
from signal import pause
import sys
import time
import datetime
from send import P2P

ON=1
OFF=0

p2p = P2P()

class GPIO():
    def __init__(self):
        self.button = gpiozero.Button(21, pull_up=True)
        self.led = gpiozero.LED(17)
        self.buz = gpiozero.Buzzer(27)
        self.status = OFF
        self.tick_status = True

    def tick(self):
         if self.status == OFF:
             self.led.off()
             self.buz.off()
         if self.status == ON:
             if self.tick_status:
                 self.led.off()
                 self.buz.off()
             else:
                 self.led.on()
                 self.buz.on()
             self.tick_status = not(self.tick_status)

    def on(self):
       self.status = ON

    def is_pressed(self):
        return self.button.is_pressed == 1

    def off(self):
       self.status = OFF
