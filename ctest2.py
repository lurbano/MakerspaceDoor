import time
import os
import subprocess
subprocess.Popen('ls -la', shell=True)
import board
import digitalio


os.system('amixer cset numid=1 100%')
os.system("cvlc --play-and-exit portal_start.mp3")


s1 = digitalio.DigitalInOut(board.D17)
s1.direction = digitalio.Direction.INPUT
s1.pull = digitalio.Pull.DOWN

isopen = s1.value


while True:
        #if (s1.value) == True:
        #       print("closed")
        #else:
        #        print("open")
        if (s1.value != isopen):
                isopen = s1.value
                if isopen == True:
                        print("closed")
                else:
                        print("open")
                        os.system("cvlc --play-and-exit bbc_comedy-sou_07005034.mp3")

        time.sleep(0.05)