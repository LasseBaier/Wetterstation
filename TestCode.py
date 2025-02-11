from machine import Pin, I2C
import time
from PASCO2V01 import PASCO2V01
from Bme280 import BME280



Button = Pin(16, Pin.IN, Pin.PULL_UP)




i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=300_000)

bme = BME280(i2c)

Pasco2 = PASCO2V01(i2c, bme, Button)

#i2c.writeto_mem(0x28, 0x04, bytes([0x02]))

# Idle mode
#Pasco2.write(0x04, 16)

#Int as interrupt
Pasco2.write(0x08, 14)

# Mesurment Period H
Pasco2.write(0x02, 0x00)
# Mesurment Period L Periode auf 6s
Pasco2.write(0x03, 0x06)

# Continuous mode
Pasco2.write(0x04, 1)

try:
    while True:
        print(bme.raw_pressure())
        print(bme.pressure)
        print(bme.raw_humidity())
        print(bme.humidity)
        print(bme.raw_temperature())
        print(bme.temperature)
        time.sleep(2)
        print(Pasco2.read_value())
        time.sleep(2)
        print(Pasco2.compensated_value())
    
        time.sleep(59)
        """Pasco2.write(0x04, 1)
        time.sleep(1)
        print("Value")
        print(Pasco2.compensated_value())
        time.sleep(1)
        print("Baseline")
        print(Pasco2.read_value_Baseline())
        time.sleep(1)"""


except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...") 