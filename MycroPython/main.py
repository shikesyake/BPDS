import socket
import time
from machine import Pin
import time
import raspi

led15 = machine.Pin(15, machine.Pin.OUT)
led = Pin(0, Pin.OUT)

raspi.wifi.ssid = 'ibaraki'
raspi.wifi.key = 'ibarakiken'
# wifiの接続
raspi.wifi.connect()

 

M_SIZE = 1024

kensyutu = 0
button = 0

# 
locaddr = ('0.0.0.0', 8890)
burocas = ('255.255.255.255',8890)
# ①ソケットを作成する
socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)
print('create socket')

# ②自ホストで使用するIPアドレスとポート番号を指定
sock.bind(locaddr)
print('Waiting message')


#if kensyutu == 1:
while True:
    try :
        # ③Clientからのmessageの受付開始
        message, cli_addr = sock.recv(M_SIZE)
        message = sock.read(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f'[{message}]を受信しました')
        if message == f"akan":
                print('起動信号を受信しました')
                led15 = 1
                led = 0
        elif message == f"tomareya":
                print('停止信号を受信しました')
                led15 = 0
                led = 1
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break
        #鳴動後停止
    except: 
        if button == 1:
            sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
            print(f'停止ボタン押下')
            #スピーカー.off的な
            button = 0
        # while True:
        #     if message != ("tomareya"):
        #         print('寺阪を受信しました')
        #         sock.sendto('寺阪を受信'.encode(encoding='utf-8'), burocas)
        #         print('受信確認を送信しました')
        #         break

        # Clientが受信待ちになるまで待つため
        time.sleep(1)

        # ④Clientへ受信完了messageを送信
        
