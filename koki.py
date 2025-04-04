import socket
import time
from send import P2P
from button import GPIO
import readchar
#from readchar import readkey, key as inchar

##############################
##                         　##
##   GPIOピンの有無問わず動作 　　　##
##                  　　      ##
#############################


raspi = False
keyboard = True
p2p = P2P()


try:
    gpio = GPIO()
    raspi = True
    print('GPIOが存在するデバイスです')
except:
    raspi = False
    print('GPIOが存在しないデバイスです')
    try:
        inputkey = readchar.readchar()
    except:
        keyboard = False
        print('キー操作不可')

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
##送信する場合はバインドを外す

#sock.bind(locaddr)
print('Waiting message')


#if kensyutu == 1:
while True:
    if raspi == True:
        if gpio.is_pressed():
            p2p.stop_alert()
            print('停止ボタン押下')
        gpio.tick()
    elif keyboard == True:
        inputkey = readchar.readchar()
        if inputkey == "t":
            p2p.stop_alert()
            print('停止ボタン押下')
            #time.sleep(0.1)
        elif inputkey == "s":
            p2p.alert()
            print('アラートボタン押下')  
    try:
        # ③Clientからのmessageの受付開始
        #time.sleep(0.2)
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(f"{cli_addr}から"f'[{message}]を受信しました')

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
                
    except socket.timeout:
        continue
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()
