from machine import Pin, I2C
import time

# Default i2c address
PASCO2V01_I2C_ADDRESS = 0x28

""" Register addresses """
# Measurement mode configuration register
MMCR = 0x04
# Idle Mode
MMCR_I = 16
# Single shot Mode
MMCR_S = 1
# Continuous mode
MMCR_C = 18
# Force baseline offset
MMCR_Base = 9

# Interrupt pin configuration register
IPCR = 0x08
# Int as Data is ready pin
Int_IPCR = 21

# Measurement period configuration register
MPCR_H = 0x02
MPCR_H = 0x03
# Period Time = 5 Sekunden
MPCR_H_P = 0
MPCR_L_P = 5

# CO2 concentration result register
CO2_HIGH = 0x05
CO2_LOW  = 0x06

# Pressure compensation registers
Pres_Ref_H = 0x0B
Pres_Ref_L = 0x0C

# Automatic baseline offset compensation reference ( Values between 350ppm and 1500ppm)
Baseline_offset_H = 0x0D
Baseline_offset_L = 0x0E


class PASCO2V01:
    def __init__(self, i2c, Bme280, Button, address = PASCO2V01_I2C_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.bme = Bme280
        self.button = Button
        self.button.irq(trigger = Pin.IRQ_RISING, handler = self.interrupt)
        
    def read(self, register):
        """Read an unsigned byte from the specified register."""
        return int.from_bytes(self.i2c.readfrom_mem(self.address, register, 1), 'big')
    
    def write(self, register, value):
        """Write an 8-bit value to the specified register."""
        b = bytearray(1)
        b[0] = value & 0xFF
        self.i2c.writeto_mem(self.address, register, b)
    
    def read_value_Baseline(self):
        msb = self.read(0x0D)
        lsb = self.read(0x0E)
        raw = (msb << 8) | lsb
        return raw    
    
    
    def read_value(self):
        msb = self.read(CO2_HIGH)
        lsb = self.read(CO2_LOW)
        raw = (msb << 8) | lsb
        return raw
    
    def compensated_value(self):
        p = self.bme.read_pressure() // 256
        pi = p // 100
        msb = pi >> 8
        lsb = pi & 0xFF
        self.write(Pres_Ref_H, msb)
        self.write(Pres_Ref_L, lsb)
        return f"{self.read_value()} ppm" 
 
    def Baseline_offset(self):
        p = self.bme.read_pressure() // 256
        data = p // 100
        time.sleep(1)
        msb = data >> 8
        lsb = data & 0xFF
        self.write(Baseline_offset_H, msb)
        self.write(Baseline_offset_L, lsb)
        
    def interrupt(self, pin):
        self.Baseline_offset()
    
    
    
    
    
    
    
    
    
    
    
        