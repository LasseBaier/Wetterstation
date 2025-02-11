from machine import SPI, Pin, I2C
from eInk import EPD
import time

spi = SPI(id=0, baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=None)

CS = Pin(5, Pin.OUT)
DC = Pin(7, Pin.OUT)
RST = Pin(1, Pin.OUT)

BUSY = Pin(0, Pin.IN, Pin.PULL_UP)



Display = EPD(spi, CS, DC, RST, BUSY)
Display.init(0)
Display.Clear()


