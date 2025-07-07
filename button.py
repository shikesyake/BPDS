import gpiozero
from signal import pause
import sys
import time
import datetime
from send import P2P
from face import FaceMeshDetector



ON=1
OFF=0

p2p = P2P()
FaceMesh = FaceMeshDetector()
def start_func():
    p2p.detect_start()

class GPIO():
    def __init__(self):
        self.button = gpiozero.Button(21, pull_up=True)
        self.gbutton = gpiozero.Button(20, pull_up=True)
        self.led = gpiozero.LED(17)
        self.gled = gpiozero.LED(22)
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
###
    
    def st_is_pressed(self):
        return self.gbutton.is_pressed == 1
    
    def stop_detect(self):
        self.gled.off()
        
    def detect(self,st_is_pressed):
        if FaceMesh.start(start_func) == 'antei':
            if st_is_pressed:
                print("起動しました")
                self.gled.on()
                p2p.detect_start()
                return("tuitade")
###

    def on(self):
       self.status = ON

    def is_pressed(self):
        return self.button.is_pressed == 1

    def off(self):
       self.status = OFF
