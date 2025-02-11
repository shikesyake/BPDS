import cv2 as cv
import mediapipe as mp



#oya.pyに組み込み、関節認識後に検知・通知機能を始動する



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# Webカメラから入力
cap = cv.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = pose.process(image)
    # 検出されたポーズの骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv.imshow('MediaPipe Pose', cv.flip(image, 1))
    if cv.waitKey(5) & 0xFF == 27:
      break
cap.release()