# main.py
import sys
import time
from face import FaceMeshDetector

# MediaPipe のモデルパス (例: 'face_detector.bin' を mediapipe assets から取得)
# 実際の環境では、以下のパスが正しく設定されていることを確認してください。
# 例: /usr/local/lib/python3.x/dist-packages/mediapipe/models/face_detector.bin
# または、models ディレクトリ内にコピーしている場合
MODEL_PATH = "./models/blaze_face_short_range.tflite"  # ここを実際のモデルファイルのパスに変更してください

def start_func():
    print("検出開始処理")
    # ここに検出開始時の具体的な処理を追加

def alert_func():
    print("アラート通知処理")
    # ここにアラート時の具体的な処理を追加

def stop_func():
    print("検出停止処理")
    # ここに検出停止時の具体的な処理を追加

if __name__ == "__main__":
    # 1. モデルファイルが存在するか確認
    import os
    if not os.path.exists(MODEL_PATH):
        print(f"エラー: モデルファイル {MODEL_PATH} が見つかりません。")
        print("mediapipe モデルをダウンロードして配置するか、パスを修正してください。")
        sys.exit(1)

    print("FaceMeshDetector を初期化しています...")
    
    try:
        detector = FaceMeshDetector(MODEL_PATH)
    except Exception as e:
        print(f"初期化エラー: {e}")
        sys.exit(1)

    print("待機モードを開始します (顔が検出されるまで待機)...")
    try:
        status = detector.start(start_func)
        
        if status == "tuitade":
            print("待機解除！メインループ開始")
            detector.run(start_func, alert_func, stop_func)
        else:
            print("待機モードで失敗しました。")
    finally:
        detector.close()
        
# import cv2 as cv
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from send import P2P
# from face import FaceMeshDetector

# # 定義
# P2Psend = P2P()
# # モデルパスの指定（実際のパスに書き換え）
# MODEL_PATH = './models/blaze_face_short_range.tflitek' 
# FaceMesh = FaceMeshDetector(model_path=MODEL_PATH)
# # バインド
# ##P2Psend.bind()

# def start_func():
#     P2Psend.detect_start()

# def alert_func():
#     P2Psend.alert()

# def stop_func():
#     P2Psend.stop_alert()

# # 実行
# # FaceMesh.cap[0].open(0) のようなコードは、FaceMeshDetector クラスの初期化および run メソッド内にある
# # FaceMesh.cap[0].open(0)
# # FaceMesh.cap[1].open(1)
# if FaceMesh.start(start_func) == 'tuitade':
#     exit
# FaceMesh.run(start_func, alert_func, stop_func)
