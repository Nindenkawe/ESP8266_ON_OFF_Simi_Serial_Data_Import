#Require modules,
from machine import Pin, UART
import json

Rx = machine.Pin(3, Pin.IN)
Tx = machine.Pin(1, Pin.OUT)
output = json.dumps(doc)

 
#json doc file
doc ={
    "doc_packet": [],
}

doc = json.dumps(doc)

file = open ('on_street_doc.json', 'a')
file.write(doc)
file.close()

doc = serial.Serial('COM3' ,115200)
time.sleep(1)


while True:
    while (doc.inWaiting() == 0):
        pass
    doc_packet = doc.readline()
    doc_packet = str(doc_packet, 'utf8')
    print(doc_packet)