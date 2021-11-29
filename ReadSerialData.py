#Require modules,
import json, serial, time
from machine import Pin, ADC
from hcsr04 import HCSR04
import time

sensor = HCSR04(trigger_pin=16, echo_pin=0)
sensor_state = True
distance = sensor.distance_cm()

while True:
    if sensor_state == True and distance > 20:
        print(" 1 slot free ")
        time.sleep_us(10)
    elif distance < 15:
        print("Parking full")
        time.sleep_us(10)
    else:
        print("offline")
        break

 
#json doc file
doc = []

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