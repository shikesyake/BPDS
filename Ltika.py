import socket
import time
import RPi.GPIO as GPIO

#GPIOkankei
led = 11
gpio_sw = 13
GPIO.setmode(GPIO.BOARD)

#in
GPIO.setup(gpio_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(0.1)
#out
GPIO.setup(led, GPIO.OUT)

GPIO.output(led, 0)
status = 0


while True:
    sw = GPIO.input(gpio_sw)
    if sw == 0:
        GPIO.output(led, 1)
        time.sleep(0.5)
    else:
        GPIO.output(led, 0)

##        if button == 1:
##            sock.sendto(b'tomareya'.encode(encoding='utf-8'),burocas)
##            print(f'停止ボタン押下')
##            
##            #スピーカー.off的な
##            button = 0
##        # while True:
##        #     if message != ("tomareya"):
##        #         print('寺阪を受信しました')
##        #         sock.sendto('寺阪を受信'.encode(encoding='utf-8'), burocas)
##        #         print('受信確認を送信しました')
##        #         break
##
##        # Clientが受信待ちになるまで待つため
##        time.sleep(1)
##
##        # ④Clientへ受信完了messageを送信
##        
##    except KeyboardInterrupt:
##        print ('\n . . .\n')
##        sock.close()
##        break
##
