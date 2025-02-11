from eInk import EPD
from machine import SPI, Pin
import time
import framebuf
import sys
from warn_layout import warn_layout

spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=None, baudrate=1_000_000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(7)
rst = Pin(1)
busy = Pin(0)

epd = EPD(spi, cs, dc, rst, busy)
epd.init(0)
epd.Clear(0xFF)
time.sleep(1)

buf = bytearray(200 * 200 // 8)
fb = framebuf.FrameBuffer(buf, 200, 200, framebuf.MONO_HLSB)
black = 0
white = 1

fb.fill(white)
fb.pixel(30, 10, black)
fb.hline(30, 30, 10, black)
fb.vline(30, 50, 10, black)
fb.line(30, 70, 40, 80, black)
fb.rect(30, 90, 10, 10, black)
fb.fill_rect(30, 110, 10, 10, black)

for row in range(0,37):
	fb.text(str(row),0,row*8,black)
fb.text('Line 36',0,200,black)
epd.display(buf)
time.sleep(1)


layout = framebuf.FrameBuffer(warn_layout,200,200, framebuf.MONO_HMSB)
#fb.blit überschreibt den gesamten buffer mit weiß und fügt den rest dazu welcher schwarz werden soll
fb.blit(layout,0,0)

epd.display(buf)
time.sleep(1)
# Send epaper to sleep
epd.sleep()
time.sleep(2)


value = 1111
# Wakeup epaper
epd.reset()
fb.text(f"Min:{value}", 30, 9, black)
fb.text(f"Max:{value}", 30, 22, black)
fb.text(f"Now:{value}", 30, 35, black)
epd.display(buf)
time.sleep(1)
epd.sleep()