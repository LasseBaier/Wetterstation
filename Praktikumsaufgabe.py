import network
from wifi_module import connect, disconnect
import config
import time
import socket
import machine
from machine import Timer, I2C, Pin
from Bme280 import BME280

Data = []
Data_buffer = []

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400_000)
bme = BME280(i2c=i2c)


def Read():
    pressure = bme.pressure
    temperature = bme.temperature
    humidity = bme.humidity
    current_time = time.localtime()
    
    timestamp = f"{current_time[3]:02}:{current_time[4]:02}:{current_time[5]:02}"  # Stunden, Minuten, Sekunden
    
    Data_buffer = [timestamp, pressure, temperature, humidity]
    
    return Data_buffer


def timer_handler(t):
    global Data
    
    if len(Data) > 100:
        Data.pop(0)
        
    Data.append(Read())
     
# Create and initialize the timer
tim = Timer()
tim.init(period=1000,  # 1 millisecond
        mode=Timer.PERIODIC,
        callback=timer_handler)


def web_page(Data):
    html = """<html>
<head>
<title>RP2040 Web Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}
p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
   border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
   .button2{background-color: #4286f4;}
   table { margin: auto; border-collapse: collapse; width: 80%; }
   th, td { border: 1px solid black; padding: 8px; text-align: center; }
   th { background-color: #f2f2f2; }
</style>
</head>
<body>
<h1>RP2040 Web Server</h1> 
<p><a href="/erase"><button class="button">Daten löschen</button></a></p>
<table>
<tr><th>Zeit</th><th>Temperatur (°C)</th><th>Luftdruck (hPa)</th><th>Luftfeuchtigkeit (%)</th></tr>"""

    # Füge die Werte aus dem Data in die HTML-Tabelle ein
    for entry in Data:
        timestamp, temp, pressure, humidity = entry
        
        # Stelle sicher, dass die Werte als Fließkommazahlen formatiert werden
        try:
            temp = (temp)  # Versuche, es als Fließkommazahl zu interpretieren
            pressure = (pressure)
            humidity = (humidity)
        except ValueError:
            temp = pressure = humidity = 0.0  # Wenn ein Fehler auftritt, setze die Werte auf 0

        # Formatierte Ausgabe
        html += f"<tr><td>{timestamp}</td><td>{temp}</td><td>{pressure}</td><td>{humidity}</td></tr>"

    # Tabelle schließen
    html += """</table><br><a href="/erase"><button style="padding:10px 20px;">Daten löschen</button></a></body></html>"""
    
    return html




def await_connection(sock):
    global Data
    print(' >> Awaiting connection ...')
    con, addr = sock.accept()
    try:
        cmd = con.recv(1024)
        if not cmd:
            print(f' >> {addr} disconnected')
            return
        else:
            request = cmd

        print(f"Received  {cmd.decode()}")
        Data_erase = str(request).find('/erase')
        
        if Data_erase != -1:  # Korrektur: Überprüfen, ob '/erase' gefunden wurde
            print('Daten löschen')
            Data = []  # Löscht die gespeicherten Daten
        
        # Antwort immer setzen
        response = web_page(Data)  # Verwende eine Kopie der Daten
        print(f"Returning {response}")
        con.send('HTTP/1.1 200 OK\n')
        con.send('Content-Type: text/html\n')
        con.send('Connection: close\n\n')
        con.sendall(response)
        
    finally:
        con.close()  # Verbindung schließen
        print(' >> Connection closed.')






if __name__ == "__main__":
    # Initialize the Wi-Fi interface in Station mode
    nic = network.WLAN(network.STA_IF)

    # Connect to SSID
    if connect(nic, config.SSID, config.PSWD):
       print("Connected to Wi-Fi!")
    else:
       print("Failed to connect.")
    print(nic.ifconfig())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Following line is preventing the error ERROR: [Errno 98] EADDRINUSE
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('0.0.0.0', 80))
        s.listen(5)

        while True:
            await_connection(s)
    except KeyboardInterrupt:
        print("Closing socket ...")
        s.close()

    except OSError as e:
        print(f' >> ERROR: {e}')
        print("Closing socket ...")
        s.close()
