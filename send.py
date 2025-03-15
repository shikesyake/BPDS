import socket
from enum import Enum
# from button import Button

# 定数
M_SIZE = 1024
burocas = ('255.255.255.255',8890)
localhost = ('127.0.0.1',8890)
localaddr = ('0.0.0.0',8890)

# メッセージの定義
class MessageData(Enum):
    START = b"kidousitade"
    ALERT = b'akan'
    STOP = b"tomareya"
    HAYOKOI = b""

class P2P:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # ブロードキャストを許可
        self.burocas = ('255.255.255.255',8890)

    def bind(self):
        self.sock.bind(localhost)
    def bindb(self):
        self.sock.bind(localaddr)


    def send(self, data):
        for i in range(3):
            try:
                self.sock.sendto(data, burocas)
            except:
                print("")
    
    #下要らんかも

    def akan(self):
        self.send(MessageData.ALERT.value)
    
    def kidou(self):
        self.send(MessageData.START.value)

    def tomareya(self):
        self.send(MessageData.STOP.value)
        
    def recv(self):
        try:
            message, cli_addr = self.sock.recvfrom(M_SIZE)
            return message
        except socket.timeout: 
            return MessageData.HAYOKOI.value