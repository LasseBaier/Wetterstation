from machine import Pin, I2C
import time
import framebuf
import sys

# 24 Hours in sec
Max_time = 24*60*60

#Clors
black = 0
white = 1

class e_lnk_controller:
    def __init__(self, EPD, BME, Pasco2):
        self.Epd = EPD
        self.bme = BME
        self.Pasco2 = Pasco2
        self.hour_buffer = []
        self.Max_time = 24*60*60
        # Min and Max Pressure
        self.Min_Max_pressure = [] 
        # Min and Max Temperature
        self.Min_Max_temperature = []  
        # Min and Max Humidity 
        self.Min_Max_humidity = [] 
        # Min and Max co2
        self.Min_Max_co2 = [] 
        #Buffer 
        self.buf = bytearray(200 * 200 // 8)
        self.min_max_buffer = framebuf.FrameBuffer(self.buf, 200, 200, framebuf.MONO_HLSB)


    def data_24_hour(self):
        pressure = self.bme.raw_pressure()
        temperature = self.bme.raw_temperature()
        humidity = self.bme.raw_humidity()
        co2 = self.Pasco2.read_value()
        now = time.time()
        
        self.hour_buffer.append((now, temperature, humidity, co2, pressure, now))
        
        # Remove outdated values
        while self.hour_buffer and self.hour_buffer[0][0] < now - Max_time:
            self.hour_buffer.pop(0)
            
    def min_max_values(self, Value):
        
        # If no Values are available
        if not self.hour_buffer:
            return None, None
        
        # copys all Values out of the 24hour_buffer from the Index in "Index"
        Values = [entry[Value] for entry in self.hour_buffer]
        return min(Values), max(Values)
    
    def show_min_max(self,temperature=1, humidity=2, co2=3, pressure=4):
        Min_Max_pressure = self.min_max_values(pressure)
        Min_Max_temperature = self.min_max_values(temperature)
        Min_Max_humidity = self.min_max_values(humidity)
        Min_Max_co2 = self.min_max_values(co2)
        
        self.min_max_buffer.fill(white)
        # show Pressure
        self.min_max_buffer.text(f"Min:{Min_Max_pressure[0]}", 30, 61, black)
        self.min_max_buffer.text(f"Max:{Min_Max_pressure[1]}", 30, 74, black)
        # show Temperature
        self.min_max_buffer.text(f"Min:{Min_Max_temperature[0]}", 130, 9, black)
        self.min_max_buffer.text(f"Max:{Min_Max_temperature[1]}", 130, 22, black)
        # show humidity
        self.min_max_buffer.text(f"Min:{Min_Max_humidity[0]}", 130, 61, black)
        self.min_max_buffer.text(f"Max:{Min_Max_humidity[1]}", 130, 74, black)
        # show co2
        self.min_max_buffer.text(f"Min:{Min_Max_co2[0]}", 30, 9, black)
        self.min_max_buffer.text(f"Max:{Min_Max_co2[1]}", 30, 22, black)
        
        self.Epd.display(self.min_max_buffer)

        
        
        
        
        
        
        
        






