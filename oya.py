import mediapipe as mp
import cv2 as cv
import socket

# burocas = ('255.255.255.0',8890)
burocas = ('broadcasthost',8890)
localhost = ('127.0.0.1',8890)
#ソケット作成
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
#通知までのカウント
count = 0

mp_drawing = mp.solutions.drawing_utils # 描画用のインスタンス
mp_face_mesh = mp.solutions.face_mesh # MLソリューションの顔メッシュインスタンス
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv.VideoCapture(0)
w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))         
fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')  
video = cv.VideoWriter('face_mesh_video.mp4', fourcc, 30, (w, h))

while cap.isOpened():
    tick = cv.getTickCount()
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv.cvtColor(cv.flip(image, 1), cv.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    
    #顔検知
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            print(face_landmarks)
            mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)
    else: #顔が消えたら
        print("顔が検出されなくなりました。")
        print("通知まで:",30 - count)
        count += 1
        if results.multi_face_landmarks: #カウント中に検出されたらリセット
            count = 0
        if count == 30: #30秒経過で通知
            print("通知しました")
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # ブロードキャストを許可
            sock.sendto('akan'.encode(encoding='utf-8'),burocas)
            count = 0
            #スピーカーオンおく

        if button == 1:
            #スピーカー.off的な
            if meido == y:
                sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
            print(f'停止ボタン押下')
            button = 0
            break #いったん検知したらbreak 継続動作するよう書き換え

        
    fps = cv.getTickFrequency() / (cv.getTickCount() - tick) # fpsの計算
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
    video.write(image)
    if cv.waitKey(5) & 0xFF == 27: # escで終了
        break
    if cv.waitKey(5) & 0xFF == 32: # spaceでスクリーンショット
        dt = datetime.datetime.now()
        cv.imwrite(dt.isoformat() + ".png", image)
face_mesh.close()
cap.release()
