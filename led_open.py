import board
import neopixel
import time

nPix = 20
pixels = neopixel.NeoPixel(board.D21, 20)

for i in range(nPix):
    pixels[i] = (0,100,0)
    time.sleep(0.1)
    