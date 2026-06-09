import sys
import time
from face import FaceMeshDetector
from send import P2P

# import cv2 as cv
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from face import FaceMeshDetector


# 定義
P2Psend = P2P()
# モデルパスの指定
MODEL_PATH = './models/blaze_face_short_range.tflite'  # 例: './models/blaze_face_short_range.tflite'
# FaceMesh = FaceMeshDetector(model_path=MODEL_PATH)
# バインド
##P2Psend.bind()

def start_func():
    P2Psend.detect_start()

def alert_func():
    P2Psend.alert()

def stop_func():
    P2Psend.stop_alert()

if __name__ == "__main__":
    # モデルファイルが存在するか確認
    import os
    if not os.path.exists(MODEL_PATH):
        print(f"モデルファイル {MODEL_PATH} が見つかりません。")
        print("mediapipe モデルをダウンロードして配置するか、パスを修正してください。")
        sys.exit(1)

    print("FaceMeshDetectorを初期化")
    
    try:
        detector = FaceMeshDetector(MODEL_PATH)
    except Exception as e:
        print(f"初期化エラー: {e}")
        sys.exit(1)

    print("顔が安定して検出され続けるまで待機...")

    # 実行
    # FaceMesh.cap[0].open(0) のようなコードは、FaceMeshDetector クラスの初期化および run メソッド内にある
    # FaceMesh.cap[0].open(0)
    # FaceMesh.cap[1].open(1)
 
    # if FaceMesh.start(start_func) == 'tuitade':
    #     exit
    # FaceMesh.run(start_func, alert_func, stop_func)
    try:
        status = detector.start(start_func)
        
        if status == "tuitade":
            print("待機解除！メインループ開始")
            detector.run(start_func, alert_func, stop_func)
        else:
            print("待機中に失敗しました。")
    finally:
        detector.close()
