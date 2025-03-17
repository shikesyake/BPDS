#　土台
import RPi.GPIO as GPIO
import time
import socket

# スピーカーのGPIOピン番号
SPEAKER_PIN = 12
BUTTON = 3


# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#a 
# classつけた
# スピーカーをオンにする関数
class Speaker:
    def __init__(self):
        self.meido = 0
        self.y = 1
        self.burocas = ('localhost', 8890)
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)         

    def speaker_on(self):
        GPIO.output(SPEAKER_PIN, GPIO.HIGH)
        print("スピーカーオン")


# スピーカーをオフにする関数
    def speaker_off(self):
        GPIO.output(SPEAKER_PIN, GPIO.LOW)
        print("スピーカーオフ")

#スピーカーを制御するインスタンスを作成
speaker = Speaker()

 # ボタンの状態を監視してスピーカーを制御するループ
button = 0 ##追加
try:
    while True:
        input_state = GPIO.input(BUTTON)
        if input_state == GPIO.LOW:  # ボタンが押された場合
            speaker.speaker_off()
            if speaker.meido == speaker.y:
                speaker.sock.sendto(b'tomareya'.encode(encoding='utf-8'), speaker.burocas)
            print(f'停止ボタン押下')
            button = 0
            break  # いったん検知したらbreak 継続動作するよう書き換え
        else:
            speaker.speaker_on()
        time.sleep(0.1)  # 0.1秒待機
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
