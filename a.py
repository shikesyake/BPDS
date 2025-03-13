import cv2


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
print(get_available_video_devices())
