import time
from send import P2P ,MessageType
import socket

sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.settimeout(0.1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # ブロードキャストを許可
localhost = ('127.0.0.1',8890)

p2p = P2P()

kensyutu = 0
button = 0
# ②自ホストで使用するIPアドレスとポート番号を指定
sock.bind(localhost)
print('Waiting message')

#LEDの点灯

#if kensyutu == 1:
while True:
    # Clientが受信待ちになるまで待つため
    time.sleep(1)
    message_type = p2p.recv()
    # p2p.recv()

    #     # ③Clientからのmessageの受付開始
    # message = message.decode(encoding='utf-8')
    # print(f'[{message}]を受信しました')

    if message_type == MessageType.START:
        print('起動信号を受信しました')
        # music = on
        # keiho = 1

    elif message_type == MessageType.STOP:
        print('停止信号を受信しました')
    
    elif message_type == MessageType.NONE:
        exit
    
    # if button == 1:
    #             sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
    #             print(f'停止ボタン押下')
    #             #スピーカー.off的な
    #             button = 0



        # while True:
        #     if message != ("tomareya"):
        #         print('寺阪を受信しました')
        #         sock.sendto('寺阪を受信'.encode(encoding='utf-8'), burocas)
        #         print('受信確認を送信しました')
        #         break