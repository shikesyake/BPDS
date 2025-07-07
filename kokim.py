import socket
import time
from send import P2P
from button import GPIO
import keyboard as kb
#子機モジュール化


# socket用変数
M_SIZE = 1024
locaddr = ('0.0.0.0', 8890)
burocas = ('255.255.255.255', 8890)

# GPIOの初期化
class koki:
    def __init__(self):
        self.p2p = P2P()
        self.raspi = False
        self.sendby = False
    def hantei(self):
        try:
            gpio = GPIO()
            self.raspi = True
            print('GPIOが存在するデバイスです')
        except ImportError:
            self.raspi = False
            print('GPIOが存在しないデバイスです')

    # ソケットの初期化
    def initialize_socket(self):
        sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.settimeout(0.1)
        print('create socket')
        sock.bind(locaddr)
        return sock

    # メッセージの処理
    def process_message(self,message, gpio, raspi):
        if message == "tuitade":
            print('親機が起動しました')
        elif message == "akan":
            print('ALERT受信')
            if raspi:
                gpio.on()
        elif message == "tomareya":
            print('STOP受信')
            if raspi:
                gpio.off()

    # メインループ
    def main_loop(self,sock, gpio, raspi):
        p2p = P2P()
        sendby = False

        while True:
            try:
                # GPIOの処理
                if raspi and gpio.is_pressed():
                    p2p.stop_alert()
                    gpio.off()
                    sendby = True
                    print('停止ボタン押下')
                if raspi:
                    gpio.tick()

                # キーボード入力の処理
                if kb.is_pressed("escape"):
                    p2p.stop_alert()
                    sendby = True
                    print('停止ボタン押下')
                    if raspi:
                        gpio.off()
                elif kb.is_pressed("space"):
                    p2p.alert()
                    sendby = True
                    print('アラートボタン押下')
                    if raspi:
                        gpio.on()
                        gpio.tick()

                # ソケットメッセージの処理
                try:
                    message, cli_addr = sock.recvfrom(M_SIZE)
                    message = message.decode(encoding='utf-8')
                    if not sendby:
                        print(f"{cli_addr}から[{message}]を受信しました")
                        process_message(message, gpio, raspi)
                    else:
                        sendby = False
                except socket.timeout:
                    continue

            except KeyboardInterrupt:
                print('\n終了します...')
                sock.close()
                break

# エントリーポイント
if __name__ == "__main__":
    koki = koki()
    gpio, raspi = koki.hantei()
    sock = koki.hantei()
    koki.main_loop(sock, gpio, raspi)