import gpiozero
import lgpio
from signal import pause
import sys
import time
import datetime
from send import P2P

ON=1
OFF=0

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

##    def button(self):
##        while True:
##            if self.button.is_pressed:
##                return 1
##            else:
##                return 0
    # def waitbutton(self):
    #     button.wait_for_press()
    def on(self):
       self.status = ON
##        else:
##            continue

##            except KeyboardInterrupt:
##                print ('\n . . .\n')
##                gpio.cleanup()
####                self.button.wait_for_press()
##            except:
##                continue



        
##      self.led.on()
##      time.sleep(3)
##      self.led.off()
        #下直す
    def is_pressed(self):
        return self.button.is_pressed == 1

    def off(self):
       self.status = OFF
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
