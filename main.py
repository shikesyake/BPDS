import sys
import time
import threading
import argparse
import tkinter as tk
import cv2 as cv
from PIL import Image, ImageTk
from face import FaceMeshDetector
from send import P2P

# import cv2 as cv
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from face import FaceMeshDetector


# 定義
# モデルパスの指定
P2Psend = P2P()
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


def run_detector_thread(detector):
    try:
        status = detector.start(start_func)
        if status == "tuitade":
            detector.run(start_func, alert_func, stop_func)
    except Exception as e:
        print(f"検出スレッド例外: {e}")

if __name__ == "__main__":
    # モデルファイルが存在するか確認
    import os
    if not os.path.exists(MODEL_PATH):
        print(f"モデルファイル {MODEL_PATH} が見つかりません。")
        print("mediapipe モデルをダウンロードして配置するか、パスを修正してください。")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gui', action='store_true', help='GUIでのオンオフと状態確認を有効にする')
    args = parser.parse_args()

    print("FaceMeshDetectorを初期化")
    try:
        # GUI モードでは OpenCV の表示を無効にする
        if args.gui:
            detector = FaceMeshDetector(MODEL_PATH, use_display=False)
        else:
            detector = FaceMeshDetector(MODEL_PATH)
    except Exception as e:
        print(f"初期化エラー: {e}")
        sys.exit(1)

    if not args.gui:
        print("顔が安定して検出され続けるまで待機...")
        try:
            status = detector.start(start_func)
            if status == "tuitade":
                print("待機解除！メインループ開始")
                detector.run(start_func, alert_func, stop_func)
            else:
                print("待機中に失敗しました。")
        finally:
            detector.close()
    else:
        # GUI モード: 検出は別スレッドで実行し、Tkinter で状態表示と制御を行う
        root = tk.Tk()
        root.title('BPDS GUI')

        status_var = tk.StringVar()
        status_var.set('準備完了')

        # レイアウト再構成: 左にコントロール、右にビデオ領域
        content_frame = tk.Frame(root)
        content_frame.pack(fill='both', expand=True, padx=10, pady=4)

        left_frame = tk.Frame(content_frame)
        left_frame.pack(side='left', fill='both', expand=True)

        right_frame = tk.Frame(content_frame)
        # 右フレームはビデオ表示時に pack する（初期は非表示）

        # ビデオ埋め込み用ウィジェット（最初は非表示）
        video_container = tk.Frame(right_frame, width=320, height=240, bd=2, relief='sunken')
        video_label = tk.Label(video_container)
        video_label.pack(fill='both', expand=True)

        def display_frame(img):
            # img: BGR numpy array
            try:
                img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                pil = Image.fromarray(img_rgb)
                pil = pil.resize((320, 240))
                photo = ImageTk.PhotoImage(pil)
                video_label.config(image=photo)
                video_label.image = photo
            except Exception:
                pass

        def show_video():
            try:
                # 右フレームを表示してウィンドウを再計算
                right_frame.pack(side='right', fill='y', padx=(8,0), pady=8)
                video_container.pack(fill='both', expand=True)
                toggle_btn.config(text='Hide Video')
                root.update_idletasks()
                # 自動でウィンドウサイズを拡張
                root.geometry('')
            except Exception:
                pass

        def hide_video():
            try:
                video_container.pack_forget()
                right_frame.pack_forget()
                toggle_btn.config(text='Show Video')
                root.update_idletasks()
                root.geometry('')
            except Exception:
                pass

        def toggle_video():
            # トグル状態を切り替える
            if str(toggle_btn.cget('text')).lower().startswith('show'):
                detector.frame_callback = lambda im: root.after(0, display_frame, im)
                show_video()
            else:
                detector.frame_callback = None
                hide_video()

        def update_status():
            try:
                cap_open = getattr(detector, 'cap', None) is not None and detector.cap.isOpened()
                alert = getattr(detector, 'alert', False)
                renzoku = getattr(detector, 'renzoku', False)
                count = getattr(detector, 'count', 0)
                s = f"カメラ:{'OK' if cap_open else '閉'}  alert:{alert}  連続:{renzoku}  count:{count}"
                status_var.set(s)
            except Exception as e:
                status_var.set(f'状態取得エラー: {e}')
            root.after(500, update_status)

        def start_btn():
            if getattr(start_btn, 'thread', None) and start_btn.thread.is_alive():
                print('検出スレッドは既に動作中です')
                return
            # 再初期化が必要な場合は detector を再生成
            t = threading.Thread(target=run_detector_thread, args=(detector,), daemon=True)
            start_btn.thread = t
            t.start()

        def alert_btn():
            try:
                detector.p2p.alert()
            except Exception:
                alert_func()

        def stop_alert_btn():
            try:
                detector.p2p.stop_alert()
            except Exception:
                stop_func()

        def stop_detection_btn():
            # GUIから検出ループを停止し、スレッド終了を待つ
            try:
                detector.stop_detection()
            except Exception:
                pass
            if getattr(start_btn, 'thread', None):
                start_btn.thread.join(timeout=1)

        # 下部フレーム: トグルを右下に表示
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill='x', side='bottom', padx=10, pady=6)
        toggle_btn = tk.Button(bottom_frame, text='Show Video', command=toggle_video)
        toggle_btn.pack(side='right')

        # run 開始時に自動的に展開して映像を埋め込むコールバック
        def on_started_callback():
            # 登録して表示する
            detector.frame_callback = lambda im: root.after(0, display_frame, im)
            root.after(0, show_video)

        detector.on_started = on_started_callback

        def close_all():
            try:
                detector.close()
            except Exception:
                pass
            root.destroy()

        # レイアウト調整: 状態ラベル上部、ボタンは左フレーム内に配置
        status_lbl = tk.Label(left_frame, textvariable=status_var, anchor='w')
        status_lbl.pack(fill='x', padx=2, pady=(6,4))

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill='x', padx=2, pady=8)

        start_button = tk.Button(btn_frame, text='Start Detection', command=start_btn, width=16)
        start_button.pack(side='left', padx=6)
        stop_det_button = tk.Button(btn_frame, text='Stop Detection', command=stop_detection_btn, width=16)
        stop_det_button.pack(side='left', padx=6)
        alert_button = tk.Button(btn_frame, text='Alert', command=alert_btn, width=12)
        alert_button.pack(side='left', padx=6)
        stop_alert_button = tk.Button(btn_frame, text='Stop Alert', command=stop_alert_btn, width=12)
        stop_alert_button.pack(side='left', padx=6)
        quit_button = tk.Button(btn_frame, text='Quit', command=close_all, width=8)
        quit_button.pack(side='right', padx=6)

        # 自動開始オプションのチェックボックス
        auto_var = tk.BooleanVar()
        auto_chk = tk.Checkbutton(left_frame, text='自動で検出を開始する', variable=auto_var)
        auto_chk.pack(anchor='w', padx=2, pady=(0,8))

        # 起動時に自動開始する
        def maybe_auto_start():
            if auto_var.get():
                start_btn()
        root.after(200, maybe_auto_start)

        update_status()
        root.protocol('WM_DELETE_WINDOW', close_all)
        root.mainloop()
