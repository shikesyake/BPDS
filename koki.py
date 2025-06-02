import socket
import time
from send import P2P
from button import GPIO
import keyboard as kb

##############################
##                         　##
##   GPIOピンの有無問わず動作 　　　##
##                  　　      ##
#############################


p2p = P2P()
# GPIOピンの有無
raspi = False
#自分が送信したか
sendby = False

# GPIOの有無を判定
try:
    gpio = GPIO()
    raspi = True
    print('GPIOが存在するデバイスです')
except:
    raspi = False
    print('GPIOが存在しないデバイスです')

M_SIZE = 1024
locaddr = ('0.0.0.0', 8890)
burocas = ('255.255.255.255',8890)
# ①ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.settimeout(0.1)
print('create socket')

# ②自ホストで使用するIPアドレスとポート番号を指定
##送信する場合はバインドを外す
sock.bind(locaddr)
print('Waiting message')

while True:
    if raspi == True:
        if gpio.is_pressed():
            p2p.stop_alert()
            gpio.off()
            sendby = True
            print('停止ボタン押下')
        gpio.tick()
        time.sleep(0.1)

    if kb.is_pressed("escape"):
        p2p.stop_alert()
        sendby = True
        print('停止ボタン押下')

        if raspi:
            gpio.off()
        time.sleep(0.1)

    elif kb.is_pressed("space"):
        p2p.alert()
        sendby = True
        print('アラートボタン押下')
        if raspi:#
            gpio.on()
            gpio.tick()
        time.sleep(0.1)

    try:
        # ③Clientからのmessageの受付開始
        #time.sleep(0.2)
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        if sendby == False:
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
        else:
            sendby = False
            time.sleep(0.1)
    except socket.timeout:
        continue
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()

# if __name__ == "__main__":
#     detector = FaceMeshDetector()
#     detector.run()