import mediapipe as mp
import cv2 as cv
from send import P2P,MessageType
from face import FaceMeshDetector

# ラズパイ用 クラス化するなら別ファイルに移動
# import sys
# import time
# import datetime
 
# import RPi.GPIO as GPIO
# BUTTON = 3

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# input_state = GPIO.input(BUTTON)
#ここまで


# 定義
p2psend = P2P()
facemesh = FaceMeshDetector()
# バインド
p2psend.bind()
def callback_bt():
    print("bloadcastでアラートを送信")
    facemesh.run(callback_bt)


# 実行
facemesh.run()
print(通知中)
if button == 1:
    
    led = 0


#スピーカーオンおく

# if button == 1:
#     #スピーカー.off的な
#     if meido == y:
#         sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
#     print(f'停止ボタン押下')
#     button = 0
#   break #いったん検知したらbreak 継続動作するよう書き換え