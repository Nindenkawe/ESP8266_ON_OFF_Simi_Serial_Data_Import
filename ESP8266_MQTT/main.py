import time
import json
from umqtt.simple import MQTTClient
import uasyncio as asyncio
from devices import Motor, Sensor, UltrasonicSensor

# --- Configure these ---
MQTT_SERVER = "192.168.1.71"
MQTT_PORT = 1883
MQTT_USER = "titeuf"
MQTT_PASSWORD = "Farm1test"
CLIENT_ID = "ESP-8266"
SENSOR_TOPIC = "esp8266/sensor_data"

# Pin definitions
MOTOR_PIN = 5
SENSOR_PIN = 4
TRIGGER_PIN = 16
ECHO_PIN = 0

# Initialize devices
motor = Motor(MOTOR_PIN)
sensor = Sensor(SENSOR_PIN)
ultrasonic_sensor = UltrasonicSensor(TRIGGER_PIN, ECHO_PIN)

# Initialize MQTT client
mqtt_client = MQTTClient(CLIENT_ID, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)

async def connect_mqtt():
    try:
        mqtt_client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print("Error connecting to MQTT:", e)

async def send_sensor_data():
    while True:
        try:
            # Read sensor data
            sensor_value = sensor.read_value()
            distance = ultrasonic_sensor.measure_distance()

            # Create a data dictionary
            data = {
                "sensor_value": sensor_value,
                "distance_cm": distance
            }

            # Publish data to MQTT
            mqtt_client.publish(SENSOR_TOPIC, json.dumps(data))
            print("Sensor data published:", data)

            await asyncio.sleep(5)  # Adjust the interval as needed

        except Exception as e:
            print("Error sending sensor data:", e)

async def main_loop():
    while True:
        # Add your motor control logic here
        motor.on()
        await asyncio.sleep(2)
        motor.off()
        await asyncio.sleep(2)

async def run():
    await connect_mqtt()
    await asyncio.gather(send_sensor_data(), main_loop())

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print("Error in main loop:", e)
