import time
import threading

from readchar import readkey, key as inchar

###############
##キーボード操作##
###############

class CheckKey():
    def __init__(self):
        #threading.Thread.__init__(self)
        self.Key = ''
        self.KeyTime = 0.0

    def run(self):
        while(True):
            self.Key = readkey()
            if self.Key == 't':
                return self.Key
            break

    def input(self,key):
        InputKey = CheckKey()
        while(True):
            if InputKey.Key:
                return InputKey.Key
            time.sleep(0.5)