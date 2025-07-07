import mediapipe as mp
import cv2 as cv
from send import P2P
from face import FaceMeshDetector
from button import GPIO

###################
# 親機のメインファイル #
##################

# 定義
P2Psend = P2P()
FaceMesh = FaceMeshDetector()
# バインド
##P2Psend.bind()
try:
    gpio = GPIO()
    raspi = True
    print('GPIOが存在するデバイスです')
except:
    raspi = False
    print('GPIOが存在しないデバイスです')


def start_func():
    P2Psend.detect_start()

def alert_func():
    P2Psend.alert()
def stop_func():
    P2Psend.stop_alert()
# 実行
# FaceMesh.cap[0].open(0)
# FaceMesh.cap[1].open(1)
if gpio.detect(start_func) == 'tuitade':
    if raspi:
        gpio.gled.on()

    exit
FaceMesh.run(start_func, alert_func, stop_func)
