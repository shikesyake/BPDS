import mediapipe as mp
import cv2 as cv
from send import P2P
from face import FaceMeshDetector

# 定義
P2Psend = P2P()
FaceMesh = FaceMeshDetector()
# バインド
##P2Psend.bind()

def start_func():
    P2Psend.tuitade()

def alert_func():
    P2Psend.akan()
def stop_func():
    P2Psend.tomareya()
# 実行
# FaceMesh.cap[0].open(0)
# FaceMesh.cap[1].open(1)
if FaceMesh.start(start_func) == 'tuitade':
    exit
FaceMesh.run(start_func, alert_func, stop_func)
