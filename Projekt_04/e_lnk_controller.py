from machine import Pin, I2C
import time
import framebuf
import sys
from normal_layout import normal_layout
from warn_layout import warn_layout

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
    
    def temperature_trend(self):
        
        """ saves all values of the temperature in temperature """
        temperature = [entry[1] for entry in self.hour_buffer]
        # calculates the average
        avg_temperature = sum(temperature) / len(temperature)
        
        
        """ Defines a temperature trend """
        current_temperature = temperature[-1]
        if current_temperature > avg_temperature // 100:
            return "rising"
        elif current_pressure < avg_temperature // 100:
            return "falling"
        else:
            return "steady"


    def weather_prediction(self):
        
        """ splits up each measured value of hour_buffer in a different array """
        humidity    = [entry[2] for entry in self.hour_buffer]
        pressure    = [entry[4] for entry in self.hour_buffer]
        
        
        """ calculates all averages """
        avg_temperature = sum(temperature) / len(temperature)
        avg_humidity    = sum(humidity) / len(humidity)
        avg_pressure    = sum(pressure) / len(pressure)
        
        
        """ defines a trend for measured value """
        current_pressure = pressure[-1]
        pressure_trend = "steady"
        if current_pressure > avg_pressure // 100:
            pressure_trend = "rising"
        elif current_pressure < avg_pressure // 100:
            pressure_trend = "falling"
        
        current_humidity = humidity[-1]
        humidity_trend = "steady"
        if current_humidity > avg_humidity // 100:
            humidity_trend = "rising"
        elif current_humidity < avg_humidity // 100:
            humidity_trend = "falling"
            
        if pressure_trend == "rising" and humidity_trend == "falling":
            return "sunny weather"
        elsif pressure_trend == "falling" and humidity_trend == "rising":
            return "rainy weather"
        else:
            return "steady"

    
    def ShowValues(self,Error, temperature=1, humidity=2, co2=3, pressure=4):
        LivePressure = self.bme.raw_pressure()
        LiveTemperature = self.bme.raw_temperature()
        LiveHumidity = self.bme.raw_humidity()
        LiveCo2 = self.Pasco2.read_value()
        
        self.Min_Max_pressure = self.min_max_values(pressure)
        self.Min_Max_temperature = self.min_max_values(temperature)
        self.Min_Max_humidity = self.min_max_values(humidity)
        self.Min_Max_co2 = self.min_max_values(co2)
        
        # Chose if warn or the normal Overlay should be displayed
        if Error = 1:
            if
            layout = framebuf.FrameBuffer(warn_layout,200,200, framebuf.MONO_HMSB)
        else:
            layout = framebuf.FrameBuffer(normal_layout,200,200, framebuf.MONO_HMSB)
        #fb.blit überschreibt den gesamten buffer mit weiß und fügt den rest dazu welcher schwarz werden soll
        fb.blit(layout,0,0)
        #self.min_max_buffer.fill(white)
        # show Pressure
        self.min_max_buffer.text(f"Min:{self.Min_Max_pressure[0]}", 30, 61, black)
        self.min_max_buffer.text(f"Max:{self.Min_Max_pressure[1]}", 30, 74, black)
        self.min_max_buffer.text(f"Max:{LivePressure}", 30, 87, black)
        # show Temperature
        self.min_max_buffer.text(f"Min:{self.Min_Max_temperature[0]}", 130, 9, black)
        self.min_max_buffer.text(f"Max:{self.Min_Max_temperature[1]}", 130, 22, black)
        self.min_max_buffer.text(f"Max:{LiveTemperature}", 130, 35, black)

        # show humidity
        self.min_max_buffer.text(f"Min:{self.Min_Max_humidity[0]}", 130, 61, black)
        self.min_max_buffer.text(f"Max:{self.Min_Max_humidity[1]}", 130, 74, black)
        self.min_max_buffer.text(f"Max:{LiveHumidity}", 130, 87, black)

        # show co2
        self.min_max_buffer.text(f"Min:{self.Min_Max_co2[0]}", 30, 9, black)
        self.min_max_buffer.text(f"Max:{self.Min_Max_co2[1]}", 30, 22, black)
        self.min_max_buffer.text(f"Max:{LiveCo2}", 30, 35, black)
        
        self.Epd.display(self.min_max_buffer)

        
        
        
        
        
        
        
        






