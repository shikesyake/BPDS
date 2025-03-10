#　土台

import RPi.GPIO as GPIO
import time


# スピーカーのGPIOピン番号
SPEAKER_PIN = 12


# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)


# スピーカーをオンにする関数
def speaker_on():
    GPIO.output(SPEAKER_PIN, GPIO.HIGH)
    print("スピーカーオン")


# スピーカーをオフにする関数
def speaker_off():
    GPIO.output(SPEAKER_PIN, GPIO.LOW)
    print("スピーカーオフ")

 # ボタンの状態を監視してスピーカーを制御するループ
try:
    while True:
        input_state = GPIO.input(BUTTON)
        if input_state == GPIO.LOW:  # ボタンが押された場合
            speaker_off()
            if meido == y:
                sock.sendto(b'tomareya'.encode(encoding='utf-8'), burocas)
            print(f'停止ボタン押下')
            button = 0
            break  # いったん検知したらbreak 継続動作するよう書き換え
        else:
            speaker_on()
        time.sleep(0.1)  # 0.1秒待機
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
