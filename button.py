
import sys
import time
import datetime
 
import RPi.GPIO as GPIO

BUTTON = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
input_state = GPIO.input(BUTTON)

def :
    button = 1


def main():
    try:
        # 操作対象のピンは「GPIOn」の"n"を指定する
        GPIO.setmode(GPIO.BCM)
        # BUTTONがつながるGPIOピンの動作は「入力」「プルアップあり」
        GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # 立ち下がり（GPIO.FALLING）を検出する（プルアップなので通常時1／押下時0）
        GPIO.add_event_detect(BUTTON, GPIO.FALLING, bouncetime=200)
        # イベント発生時のコールバック関数を登録
        GPIO.add_event_callback(BUTTON, button_pressed)
         
           # 無限ループ
        while True:
            # 主処理は何もしない
            time.sleep(1)
    except KeyboardInterrupt:
        print(error)
       # GPIOの設定をリセット
    GPIO.cleanup()
     
    return 0

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
