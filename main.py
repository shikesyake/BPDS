import mediapipe as mp
import cv2 as cv
from send import P2P,MessageData
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
P2Psend = P2P()
FaceMesh = FaceMeshDetector()
# バインド
P2Psend.bind()


def alert_func():
    print("コールバックalertを実行")
    P2Psend.akan()
def start_func():
    P2Psend.kidou()
def stop_func():
    P2Psend.tomareya()

# 実行
# FaceMesh.cap[0].open(0)
# FaceMesh.cap[1].open(1)
if FaceMesh.start(start_func) == 'kidou':
    FaceMesh.run(start_func,alert_func,stop_func)
#スピーカーオンおく

# if button == 1:
#     #スピーカー.off的な
#     if meido == y:
#         sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
#     print(f'停止ボタン押下')
#     button = 0
#   break #いったん検知したらbreak 継続動作するよう書き換え
