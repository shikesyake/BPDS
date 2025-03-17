import time
import gpiozero
##import socket
##import time
##from send import P2P
##from button import GPIO
##
##gpio = GPIO()
##p2p = P2P()
button = gpiozero.Button(19, pull_up=True)
led = gpiozero.LED(17)

while True:
    if button.is_pressed:
        print("Button is pressed")
        led.on()
        time.sleep(3)
    else:
        print("Button is not pressed")
        led.off()
        time.sleep(1)
