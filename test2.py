from machine import Pin, I2C, SPI
import time
from PASCO2V01 import PASCO2V01
from Bme280 import BME280
from eInk import EPD
import framebuf
from Projekt_04.e_lnk_controller import e_lnk_controller

# Initialize Button
Button = Pin(16, Pin.IN, Pin.PULL_UP)
# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=300_000)

# Initialize SPI and EPD
spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=None, baudrate=1_000_000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(7)
rst = Pin(1)
busy = Pin(0)
epd = EPD(spi, cs, dc, rst, busy)
epd.init(0)

# Create BME object
bme = BME280(i2c)

# Create Pasco2 object
Pasco2 = PASCO2V01(i2c, bme, Button)

Display=e_lnk_controller(epd, bme, Pasco2)

epd.reset()


for i in range(10):
    Display.data_24_hour()
    print(Display.hour_buffer)
    time.sleep(5)
    
Display.show_min_max()


