import socket
from enum import Enum
# from button import Button

# 定数
M_SIZE = 1024
burocas = ('255.255.255.255',8890)
localhost = ('127.0.0.1',8890)
localaddr = ('0.0.0.0',8890)

# メッセージの定義
# class MessageData(Enum):
#     START = 'kidousitade'
#     ALERT = 'akan'
#     STOP = 'tomareya'
#     HAYOKOI = ''

class P2P:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.settimeout(0.2)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # ブロードキャストを許可
        self.burocas = ('255.255.255.255',8890)
        self.localhost = ('127.0.0.1',8890)
        self.localaddr = ('0.0.0.0',8890)

    def bind(self):
        self.sock.bind(localhost)
    def bindb(self):
        self.sock.bind(localaddr)


    def alert(self):
        self.sock.sendto(b'akan', burocas)
    def detect_start(self):
        self.sock.sendto(b"tuitade", burocas)
    def stop_alert(self):
        self.sock.sendto(b"tomareya", burocas)

    def send(self, data):
        for i in range(3):
            try:
                self.sock.sendto(data, burocas)
                break
            except:
                print("失敗")
                continue


        
##    def recv(self):
##        try:
##            message, cli_addr = self.sock.recvfrom(1024)
##            message = message.decode(encoding='utf-8')
##            return f'{message}'
##        except socket.timeout:
##            return "None"
##        except KeyboardInterrupt:
##            print ('\n . . .\n')
##            self.sock.close()
