import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from send import P2P
from face import FaceMeshDetector

# 定義
P2Psend = P2P()
# モデルパスの指定（実際のパスに書き換え）
MODEL_PATH = './models/blaze_face_short_range.tflitek' 
FaceMesh = FaceMeshDetector(model_path=MODEL_PATH)
# バインド
##P2Psend.bind()

def start_func():
    P2Psend.detect_start()

def alert_func():
    P2Psend.alert()

def stop_func():
    P2Psend.stop_alert()

# 実行
# FaceMesh.cap[0].open(0) のようなコードは、FaceMeshDetector クラスの初期化および run メソッド内にある
# FaceMesh.cap[0].open(0)
# FaceMesh.cap[1].open(1)
if FaceMesh.start(start_func) == 'tuitade':
    exit
FaceMesh.run(start_func, alert_func, stop_func)
