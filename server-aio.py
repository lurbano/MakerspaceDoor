import asyncio
from aiohttp import web, ClientSession
from datetime import datetime
import json
from uAio import *

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

homedir = os.path.dirname(os.path.abspath(__file__))

async def handle(request):
    with open("index.html", "r") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

async def handlePost(request):
    data = await request.json()
    rData = {}
    print(data)
    # print(data["action"], data["value"])

    if data['action'] == "getTime":
        now = datetime.now()
        print(now.ctime())
        rData['item'] = "time"
        rData['status'] = now.ctime() # a string representing the current time

    if data['action'] == "getDoor":
        now = datetime.now()

        print(now.ctime())
        rData['item'] = "getDoor"
        rData['status'] = s1.value 

    
    response = json.dumps(rData)
    print("Response: ", response)
    return web.Response(text=response, content_type='text/html')

# print "Hello" every 1 second (testing async)
async def print_hello():
    while True:
        print("Hello")
        await asyncio.sleep(1)

async def doorSensor():
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
    await asyncio.sleep(0.1)

# door sensor
s1 = digitalio.DigitalInOut(board.D17)
s1.direction = digitalio.Direction.INPUT
s1.pull = digitalio.Pull.DOWN

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_post("/", handlePost)

    runner = web.AppRunner(app)
    await runner.setup()

    host = getIP()
    site = web.TCPSite(runner, host, 8080)  # Bind to the local IP address
    await site.start()
    print(f"Server running at http://{host}:8080/")

    asyncio.create_task(doorSensor())

    # startup sound
    os.system(f"sudo python3 {homedir}/led_startup.py &")
    os.system('amixer cset numid=1 100%')
    os.system(f"cvlc --play-and-exit {homedir}/portal_start.mp3")

    asyncio.create_task(print_hello())
    # asyncio.create_task(getLightLevel(dt=5))

    '''Testing post request'''
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")

    await asyncio.Event().wait()  # Keep the event loop running

if __name__ == '__main__':
    asyncio.run(main())
