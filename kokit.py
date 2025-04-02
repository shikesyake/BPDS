import socket
import time
from send import P2P
from button import GPIO

gpio = GPIO()
p2p = P2P()

START = f'kidousitade'
ALERT = f'akan'
STOP = f'tomareya'
HAYOKOI = f''

M_SIZE = 1024
localaddr = ('0.0.0.0', 8890)
burocas = ('255.255.255.255',8890)
# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.settimeout(0.01)
print('create socket')
sock.bind(localaddr)


while True:
    if gpio.is_pressed():
        p2p.tomareya()
        print('停止ボタン押下')
    gpio.tick()
    try:
        # ③Clientからのmessageの受付開始
        time.sleep(0.2)
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f"{cli_addr}から"f'[{message}]を受信しました')

        if message == "tuitade":
            print('親機が起動しました')
        elif message == "akan":
            print('ALERT受信')
            gpio.on()
        elif message == "tomareya":
            print('STOP受信')
            gpio.off()
            #鳴動後停止

        
    except socket.timeout:
        continue
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()






###########################
##                       ##  
##      旧独立版子機       ##
##                       ##       
###########################



##    if data == f"akan":
##        print('ALERT受信')
##        gpio.on()
##    elif data == f"tomareya":
##        print('STOP受信')
##        gpio.off()
##    elif data == f"kidousitade":
##        print('親機が起動しました')
##    else:
##        None



# gpio = GPIO()
# M_SIZE = 1024

# kensyutu = 0
# button = 0
# # 
# locaddr = ('0.0.0.0', 8890)
# burocas = ('255.255.255.255',8890)
# # ①ソケットを作成する
# sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
# sock.settimeout(0.1)
# print('create socket')

# # ②自ホストで使用するIPアドレスとポート番号を指定
# sock.bind(locaddr)
# print('Waiting message')


# #if kensyutu == 1:

# while True:
#     try :
#         # ③Clientからのmessageの受付開始
#         message, cli_addr = sock.recvfrom(M_SIZE)
#         message = message.decode(encoding='utf-8')
#         print(f'[{message}]を受信しました')
#         if message == f"akan":
#                 print('起動信号を受信しました')
#                 gpio.led()
#                 gpio.waitbutton()
#         elif message == f"tomareya":
#                 print('停止します')
#                 gpio.off()
#         #鳴動後停止
#         elif message == f"kidousitade":
#                 print('親機が起動しました')
#     except socket.timeout:
#         GPIO.output(led, 0)

#         if gpio.button == 1:
#             def 
#             sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
#             print(f'停止ボタン押下')
            
#             #スピーカー.off的な
#             button = 0
#         # while True:
#         #     if message != ("tomareya"):
#         #         print('寺阪を受信しました')
#         #         sock.sendto('寺阪を受信'.encode(encoding='utf-8'), burocas)
#         #         print('受信確認を送信しました')
#         #         break

#         # Clientが受信待ちになるまで待つため
#         time.sleep(1)

#         # ④Clientへ受信完了messageを送信
        
#     except KeyboardInterrupt:
#         print ('\n . . .\n')
#         sock.close()
#         break
