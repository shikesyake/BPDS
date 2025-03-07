import socket
from enum import Enum

# 定数
M_SIZE = 1024
burocas = ('255.255.255.255',8890)
localhost = ('127.0.0.1',8890)
localaddr = ('0.0.0.0',8890)

# メッセージの定義
class MessageType(Enum):
    START = b'akan'
    STOP = b"tomareya"
    NONE = b""

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

    def send(self, message_type):
        self.sock.sendto(message_type.value, burocas)
    
    #下要らんかも

    def akan(self):
        try:
            self.sock.sendto('akan'.encode(encoding='utf-8'),burocas)
        except:
            self.sock.sendto('akan'.encode(encoding='utf-8'),burocas)
    def recv(self):
        try:
            message, cli_addr = self.sock.recvfrom(M_SIZE)
            # message = message.decode(encoding='utf-8')
            # message, cli_addr = self.sock.recvfrom(M_SIZE)
            if message == MessageType.START.value:
                return MessageType.START
            elif message == MessageType.STOP.value:
                return MessageType.STOP
        except socket.timeout: 
            return MessageType.NONE
        #test
        self.sock.sendto('Success'.encode(encoding='utf-8'), cli_addr)
