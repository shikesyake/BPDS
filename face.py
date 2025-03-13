import mediapipe as mp
import cv2 as cv
import time
from send import P2P, MessageType
# ラズパイ用
# import RPi.GPIO as GPIO

#GPIOkankei
led = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
        

class FaceMeshDetector:
    def __init__(self):
        self.P2Psend = P2P()
        self.count = 0
        self.mp_drawing = mp.solutions.drawing_utils  # 描画用のインスタンス
        self.mp_face_mesh = mp.solutions.face_mesh  # MLソリューションの顔メッシュインスタンス
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        for i in range(10):
            
            self.cap += cv.VideoCapture
        self.cap = (cv.VideoCapture(0))
        self.w = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))         
        self.fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')  
        self.video = cv.VideoWriter('face_mesh_video.mp4', self.fourcc, 30, (self.w, self.h))

        # self.cap2 = cv.VideoCapture(1)
        # self.w2 = int(self.cap2.get(cv.CAP_PROP_FRAME_WIDTH))
        # self.h2 = int(self.cap2.get(cv.CAP_PROP_FRAME_HEIGHT))         
        # self.fourcc2 = cv.VideoWriter_fourcc('m', 'p', '4', 'v')  
        # self.video2 = cv.VideoWriter('face_mesh_video2.mp4', self.fourcc2, 30, (self.w2, self.h2))
 
    # def cap(self):
    #     self.cap = cv.VideoCapture(0)
    #     self.cap1 = self.cap(self.capture)

def get_available_video_devices(max_video_devices: int = 10) -> list[int]:
    """
    利用可能なビデオデバイスのリストを取得する。

    :param max_video_devices: チェックする最大のデバイス番号
    :return: 利用可能なビデオデバイスの番号のリスト
    """
    available_video_devices: list[int] = []

    for i in range(max_video_devices):
        cap: cv2.VideoCapture = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print(f"カメラが利用できません: {i}")
        else:
            print(f"カメラが利用できます: {i}")
            available_video_devices.append(i)
        cap.release()
        return available_video_devices
    

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
                GPIO.output(led, 0)
##                time.sleep(0.05)
            else:
                print("顔が検出されなくなりました。")
                print("通知まで:", 20 - self.count)
                self.count += 1
                
                time.sleep(0.1)
                if results.multi_face_landmarks:
                    self.count = 0
                    
                if self.count == 20:
                    print("通知しました")
                    GPIO.output(led, 1)
                    
                    self.P2Psend.akan()
                    # self.burocas = ('broadcasthost',8890)
                    # self.sock.sendto('akan'.encode(encoding='utf-8'),self.burocas)
                    time.sleep(0.5)
##                    GPIO.output(led, 0)
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
