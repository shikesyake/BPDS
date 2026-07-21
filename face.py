# face.py
import mediapipe as mp
import cv2 as cv
import time
import os
from send import P2P

# MediaPipe の最新 (tasks) モジュールのインポート
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class FaceMeshDetector:
    def __init__(self, model_path: str, use_display: bool = True, frame_callback=None, on_started=None):
        self.count = 0
        self.alert = False
        self.renzoku = True
        self._running = False
        self.use_display = use_display
        self.frame_callback = frame_callback
        self.on_started = on_started
        self.p2p = P2P()
        
        # MediaPipe FaceDetector の初期化
        # モデルパスの確認
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"モデルファイルが見つかりません: {model_path}")
            
        # BaseOptions の作成
        base_options = python.BaseOptions(model_asset_path=model_path)
        
        # FaceDetectorOptions の作成 (ドキュメント推奨設定)
        face_detector_options = vision.FaceDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_detection_confidence=0.5,
            min_suppression_threshold=0.3
        )
        
        # Detector の作成
        self.detector = vision.FaceDetector.create_from_options(face_detector_options)
        
        # カメラ設定
        self.cap = cv.VideoCapture(0)
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        if self.use_display:
            self.fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
            try:
                self.video = cv.VideoWriter('face_detector_video.mp4', self.fourcc, 30, (512, 288))
            except Exception:
                self.video = None
        else:
            self.video = None
    
    def get_available_video_devices(self, max_video_devices: int = 10):
        """
        利用可能なビデオデバイスのリストを取得する。

        :param max_video_devices: チェックする最大のデバイス番号
        :return: 利用可能なビデオデバイスの番号のリスト
        """
        available_video_devices = []

        for i in range(max_video_devices):
            cap = cv.VideoCapture(i)
            if not cap.isOpened():
                print(f"カメラが利用できません: {i}")
                continue
            else:
                print(f"カメラが利用できます: {i}")
                available_video_devices.append(i)
            cap.release()
        
        return available_video_devices

    def process_frame(self, image):
        """
        画像を処理し、顔検出結果を返す
        :param image: numpy 配列 (BGR)
        :return: FaceDetectorResult, 描画済み画像
        """
        
        # MediaPipe Image オブジェクトへの変換
        # 入力画像は BGR なので RGB に変換
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        
        # IMAGE モードで同期推論を実行する
        detection_result = self.detector.detect(mp_image)

        # 検出結果のリストを取り出してループ (存在しない場合は空リスト)
        detections = detection_result.detections or []
        for face_detection in detections:
            # バウンディングボックスの描画
            top_left = (int(face_detection.bounding_box.origin_x), int(face_detection.bounding_box.origin_y))
            bottom_right = (int(face_detection.bounding_box.origin_x + face_detection.bounding_box.width), 
                            int(face_detection.bounding_box.origin_y + face_detection.bounding_box.height))
            cv.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

            # 顔のポイント描画 (存在する場合のみループ)
            for point in getattr(face_detection, 'keypoints', []):
                pt = (int(point.x), int(point.y))
                cv.circle(image, pt, 5, (0, 0, 255), -1)

        # 画像の縮小
        image = cv.resize(image, dsize=(512, 288))
        
        return detection_result, image

    def close(self):
        """検出器とカメラ資源を明示的に解放する。"""
        if getattr(self, "detector", None) is not None:
            self.detector.close()
            self.detector = None
        if getattr(self, "video", None) is not None:
            try:
                self.video.release()
            except Exception:
                pass
            self.video = None
        if getattr(self, "cap", None) is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        if self.use_display:
            try:
                cv.destroyAllWindows()
            except Exception:
                pass

    def start(self, start_func):
        """
        検出を開始するまでの待機ロジック
        """
        self.runcount = 0
        self._running = True
        while self._running and self.cap.isOpened():
            tick = cv.getTickCount()
            success, image = self.cap.read()
            if not success:
                continue
            
            results, image = self.process_frame(image)

            # 検出の有無を一度だけ評価して使い回す
            has_face = bool(getattr(results, 'detections', None))
            if has_face:
                print("起動まで", 5 - self.runcount)
                self.runcount += 1
                time.sleep(1)
                if self.runcount == 5:
                    print("検知開始")
                    self.p2p.detect_start()
                    # notify that run will start
                    try:
                        if callable(self.on_started):
                            self.on_started()
                    except Exception:
                        pass
                    return "tuitade"
            else:
                # 検出されない場合はリセット
                self.runcount = 0
        
        return "fail"

    def run(self, start_func, alert_func, stop_func):
        """
        メインの検出ループ
        """
        self._running = True
        while self._running and self.cap.isOpened():
            tick = cv.getTickCount()
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                print("カメラが使用できません。")
                print("通知まで:", 20 - self.count)
                self.count += 1
                if self.count == 20:
                    print("通知しました")
                    self.p2p.alert()
                continue

            results, image = self.process_frame(image)

            # フレームコールバック（GUI用）
            try:
                if callable(self.frame_callback):
                    # 渡すのはBGRのnumpy配列
                    self.frame_callback(image.copy())
            except Exception:
                pass

            has_face = bool(getattr(results, 'detections', None))
            if has_face:
                # 顔が検出された場合にのみリセット処理
                if not self.renzoku:
                    self.count = 0
                    print("タイマーをリセットしました")
                    self.renzoku = True
                    self.alert = False
            else:
                # 顔が検出されなくなった場合のカウント処理
                if not self.alert == True:
                    print("顔が検出されなくなりました。")
                    print("通知まで:", 20 - self.count)
                    self.count += 1
                    time.sleep(0.1)
                    self.renzoku = False
                if self.count >= 20 and not self.alert:
                    print("通知しました")
                    self.p2p.alert()
                    self.count = 0
                    self.alert = True
                
            fps = cv.getTickFrequency() / (cv.getTickCount() - tick)
            cv.putText(
                image, 
                "FPS: " + str(int(fps)), 
                (image.shape[1] - 150, 40), 
                cv.FONT_HERSHEY_PLAIN, 
                2, 
                (0, 255, 0),
                2,
                cv.LINE_AA)
            # 表示や保存は use_display が True の場合のみ行う
            if self.use_display:
                try:
                    cv.imshow('MediaPipe FaceDetector', image)
                except Exception:
                    pass
                if getattr(self, 'video', None) is not None:
                    try:
                        self.video.write(image)
                    except Exception:
                        pass
                try:
                    key = cv.waitKey(5) & 0xFF
                except Exception:
                    key = None
                if key == 27:  # esc で終了
                    break
                if key == 32:  # space でスクリーンショット
                    dt = time.strftime("%Y%m%d_%H%M%S")
                    try:
                        cv.imwrite(f"./pics/{dt}.png", image)
                    except Exception:
                        pass
        
        if getattr(self, "video", None) is not None:
            try:
                self.video.release()
            except Exception:
                pass
        if getattr(self, "cap", None) is not None:
            try:
                self.cap.release()
            except Exception:
                pass
        if self.use_display:
            try:
                cv.destroyAllWindows()
            except Exception:
                pass

    def stop_detection(self):
        """外部から検出ループを止める。"""
        self._running = False
        try:
            if getattr(self, 'cap', None) is not None:
                self.cap.release()
        except Exception:
            pass