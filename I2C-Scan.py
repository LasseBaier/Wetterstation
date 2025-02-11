from machine import I2C
from machine import Pin

# Init I2C using pins GP20 & GP21 (I2C0 pins)
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400_000)

addrs_matrix = 	[["RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----", "----"],
                 ["----", "----", "----", "----", "----", "----", "----", "----", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: ", "RA: "],]

header_x = [".0  ", ".1  ", ".2  ", ".3  ", ".4  ", ".5  ", ".6  ", ".7  ", ".8  ", ".9  ", ".a  ", ".b  ", ".c  ", ".d  ", ".e  ", ".f  "]
hexa_y   = ["0x0.:", "0x1.:", "0x2.:", "0x3.:", "0x4.:", "0x5.:", "0x6.:", "0x7.:"]

print("Scanning I2C... ", end="")
detected_addresses = i2c.scan()
print(f"{len(addrs_matrix)} device(s) detected")

# 0x76 Adresse des BME280
# 0x68 Adresse des DS3231
# Die anderen Adressen sind die des Displays ((aufjedenfall ist 0x3c eine des Displays), 0x57, 0x5f)


def WerteInMatrixEinfügen(addrs_matrix, detected_addresses):
    for address in detected_addresses:
        row = address // 16  #Durch teilen des dezimalen Wertes der Adresse durch 16 erhält mann die Zeile der Adresse
        col = address % 16 #Durch Modulo erhält man den Rest des dezimalen Wertes z.B. 60&16=12 daraus kann man schließen, das die Adresse in die Spalte 12 gehört
        if addrs_matrix[row][col] != "RA:  ": #Durch die if abfrage wird geklährt ob die Adresse reserviert ist
            addrs_matrix[row][col] = f"0x{address:02X}"
        else:
            print("address is reserved")
            
                      
WerteInMatrixEinfügen(addrs_matrix, detected_addresses) #Die Funktion zur abfrage wird aufgerufen um die matrix mit den Adressen zu füllen, welche durch die .scan() funktion erhalten wurden

#Quelle die ".join" Funktion habe ich mir durch chatGPT erzeugen lassen
print("      " + " | ".join(header_x))  #.join(header) geht das header Array durch und und hängt vor jeden Wert ein "|", anschließen werden alle Einträge aus dem Array geprintet
for i, row in enumerate(addrs_matrix):  # in i wird der Zeilen wert gespeichrt und in row das Array des Zeilen wertes
    print(f"{hexa_y[i]} " + " | ".join(row)) # in der print anweißung wird erst der i. Wert des Arrays hexa_y ausgegeben und dann wird das in row gespeicherte array durchgegangen und zwischen jeden Wert ein "|" gehängt. 