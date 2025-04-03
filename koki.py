import socket
import time

##############################
## GPIOピンを持たないデバイス用  ##
##        独立動作可能       ##
#############################
M_SIZE = 1024

kensyutu = 0
button = 0
# 
locaddr = ('0.0.0.0', 8890)
burocas = ('255.255.255.255',8890)
# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.settimeout(0.1)
print('create socket')

# ②自ホストで使用するIPアドレスとポート番号を指定
sock.bind(locaddr)
print('Waiting message')


#if kensyutu == 1:
while True:
    try :
        # ③Clientからのmessageの受付開始
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f"{cli_addr}から"f'[{message}]を受信しました')
        
        if message == "tuitade":
            print('親機が起動しました')
        elif message == "akan":
            print('ALERT受信')
        elif message == "tomareya":
            print('STOP受信')
        # while True:
        #     if message != ("tomareya"):
        #         print('寺阪を受信しました')
        #         sock.sendto('寺阪を受信'.encode(encoding='utf-8'), burocas)
        #         print('受信確認を送信しました')
        #         break

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
        break
