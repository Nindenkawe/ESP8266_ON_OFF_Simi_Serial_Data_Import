from hcsr04 import HCSR04
from time import sleep


sensor_data = ""
sensor_state = True
def read_sensor_state(sensor_data):
    sensors = HCSR04(trigger_pin=16, echo_pin=0)
    if sensors.distance_cm() > 20:
        sensor_data = "1 slot free"
        sleep(2)
    elif sensors.distance_cm() <= 15:
        sensor_data = "parking full"
        sleep(2)
    else:
        print("Offline")
    return sensor_data
while True:
    read_sensor_state(sensor_data)