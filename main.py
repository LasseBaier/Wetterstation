from machine import Pin, I2C
import time
from PASCO2V01 import PASCO2V01
from Bme280 import BME280

"""_____Variables_____"""

# 24 Hours in sec
Max_time = 24*60*60
# 7 Days in sec
Max_data_time = 24*60*60*7
# Sensor Daten
Data_buffer = []
# Sensor Daten für 
hour_buffer = []
# Min and Max Pressure
Min_Max_pressure = 0
# Min and Max Temperature
Min_Max_temperature = 0
# Min and Max Humidity
Min_Max_humidity= 0
# Min and Max co2
Min_Max_co2 = 0



# Initialize Button
Button = Pin(16, Pin.IN, Pin.PULL_UP)

# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=300_000)

# Create BME object
bme = BME280(i2c)

# Create Pasco2 object
Pasco2 = PASCO2V01(i2c, bme, Button)

"""_____Functions_____"""

def data_24_hour():
    pressure = bme.raw_pressure()
    temperature = bme.raw_temperature()
    humidity = bme.raw_humidity()
    co2 = Pasco2.read_value()
    now = time.time()
    
    hour_buffer.append((timestamp, temperature, humidity, co2, pressure, now))
    
    # Remove outdated values
    while hour_buffer and hour_buffer[0][0] < now - Max_time:
        sensor_data.pop(0)
    

def add_data_to_buffer():
    pressure = bme.pressure
    temperature = bme.temperature
    humidity = bme.humidity
    co2 = compensated_value()
    current_time = time.localtime()
    now = time.time()
    
    timestamp = f"{current_time[2]:02}.{current_time[1]:02}.{current_time[0]:04}  {current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}"  # Tag.Monat.Jahr  Stunden:Minuten:Sekunden
        
    Data_buffer.append((now, timestamp, temperature, humidity, co2, pressure))
    
    # Remove outdated values
    while Data_buffer and Data_buffer[0][0] < now - Max_data_time:
        sensor_data.pop(0)
        
def Min_Max_values(Index):
    
    # If no Values are available
    if not hour_buffer:
        return None, None
    
    # copys all Values out of the 24hour_buffer from the Index in "Index"
    Values = [entry[Value] for entry in hour_buffer]
    return min(Values), max(Values)
    
    
    
