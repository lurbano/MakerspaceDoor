from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import subprocess
import time
from urllib.parse import quote
import socket 
import board
import digitalio
import random
import glob

from datetime import datetime

port = 8000
hostname=socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

print(f"Serving from: http://{hostname}.local:{port}")
print(f"at IP: http://{ipAddr}:{port}")

with open("log.txt","w") as f:
     f.write(f"Serving from: http://{hostname}.local:{port} at IP: http://{ipAddr}:{port}")
    

''' Function to convert the post data to an array for easier use'''
def postDataToArray(postData):
    raw_text = postData.decode("utf8")
    print("Raw")
    data = json.loads(raw_text)
    return data


''' Handle GET and POST requests to the server'''
class uHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = postDataToArray(post_data)
        '''
        data consists of 
            data['action'] and 
            data['value']
        '''
        self._set_headers()
        print(data)
        rData = {}
        rData['item'] = ""
        rData['status'] = ""
        
        
        if data['action'] == "getDoor":
            now = datetime.now()


            print(now.ctime())
            rData['item'] = "getDoor"
            rData['status'] = s1.value 

 

        self.wfile.write(bytes(json.dumps(rData), 'utf-8'))


httpd = HTTPServer(('', port), uHTTPRequestHandler)
# httpd.serve_forever()

os.system(f"sudo python3 /home/pi/MakerspaceDoor/led_startup.py &")

os.system('amixer cset numid=1 100%')
os.system("cvlc --play-and-exit /home/pi/MakerspaceDoor/portal_start.mp3")
# subprocess.Popen('amixer cset numid=1 100%', shell=True)
# subprocess.Popen("cvlc --play-and-exit /home/pi/portal/portal_start.mp3", shell=True)


# filelist = os.listdir("/home/pi/portal/Sounds/*.mp3")
filelist = glob.glob ("/home/pi/MakerspaceDoor/Sounds/*.mp3")
print(filelist)


s1 = digitalio.DigitalInOut(board.D17)
s1.direction = digitalio.Direction.INPUT
s1.pull = digitalio.Pull.DOWN

isopen = s1.value
print (isopen)

while True:
    httpd.handle_request()
    if (s1.value != isopen):
        isopen = s1.value
        if isopen == True:
                print("closed")
                os.system(f"sudo python3 /home/pi/door/led_close.py &")
        else:
                print("open")
                os.system(f"sudo python3 /home/pi/door/led_open.py &")
                soundFile = f"{random.choices(filelist, weights = (1, 30, 10), k = 1)[0]}"
                cmd = f"cvlc --play-and-exit {soundFile}"
                print ("sound",cmd)
                os.system(cmd)
    time.sleep(0.1)


# while True:
#     httpd.handle_request()
#     now = time.localtime()
#     print(f"Time: {now.tm_hour}:{now.tm_min} | {alarmTime.hr}:{alarmTime.min}")
#     if (now.tm_hour == alarmTime.hr) and (now.tm_min == alarmTime.min) and not alarmOn:
#         print("We have alarm!")
#         alarmOn = True 
#         rhythmboxCommand("play")
