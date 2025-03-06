import mediapipe as mp
import cv2 as cv
import time
from send import P2P, MessageType
# ラズパイ用
# import sys
# import time
# import datetime

# import RPi.GPIO as GPIO
# BUTTON = 3

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# input_state = GPIO.input(BUTTON)

class FaceMeshDetector:
    def __init__(self):
        self.P2Psend = P2P()
        self.count = 0
        self.mp_drawing = mp.solutions.drawing_utils  # 描画用のインスタンス
        self.mp_face_mesh = mp.solutions.face_mesh  # MLソリューションの顔メッシュインスタンス
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.cap = cv.VideoCapture(0)
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))         
        self.fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')  
        self.video = cv.VideoWriter('face_mesh_video.mp4', self.fourcc, 30, (self.w, self.h))
    
    # def cap(self):
    #     self.cap = cv.VideoCapture(0)
    #     self.cap1 = self.cap(self.capture)

    def process_frame(self, image):
        
        image = cv.cvtColor(cv.flip(image, 1), cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.face_mesh.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        return results, image

    def draw_landmarks(self, image, face_landmarks):
        for face_landmarks in face_landmarks.multi_face_landmarks:
            print(face_landmarks)
            self.mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)

    def run(self):
        while self.cap.isOpened():
            tick = cv.getTickCount()
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            results, image = self.process_frame(image)

            if results.multi_face_landmarks:
                self.draw_landmarks(image, results)
                time.sleep(0.05)
            else:
                print("顔が検出されなくなりました。")
                print("通知まで:", 30 - self.count)
                self.count += 1
                if results.multi_face_landmarks:
                    self.count = 0
                if self.count == 30:
                    print("通知しました")
                    self.P2Psend.akan()
                    # self.burocas = ('broadcasthost',8890)
                    # self.sock.sendto('akan'.encode(encoding='utf-8'),self.burocas)
                    self.count = 0
                    # time.sleep(0.1)

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
            cv.imshow('MediaPipe FaceMesh', image)
            self.video.write(image)
            if cv.waitKey(5) & 0xFF == 27:  # escで終了
                break
            if cv.waitKey(5) & 0xFF == 32:  # spaceでスクリーンショット
                dt = datetime.datetime.now()
                cv.imwrite(dt.isoformat() + ".png", image)
        self.face_mesh.close()
        self.cap.release()

if __name__ == "__main__":
    detector = FaceMeshDetector()
    detector.run()