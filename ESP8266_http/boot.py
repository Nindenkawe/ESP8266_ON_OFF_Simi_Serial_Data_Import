import network
import time
from machine import Pin, reset
import sys
from main import run  # Directly import the run function from main.py

# WiFi credentials
SSID = ""
PASSWORD = ""

# Pin definitions for health check
MOTOR_PIN = 5
TRIGGER_PIN = 16
ECHO_PIN = 0

# Retry limits
WIFI_RETRY_LIMIT = 5

# Function to check if devices are connected
def check_devices():
    try:
        motor_pin = Pin(MOTOR_PIN, Pin.OUT)
        sensor_trigger_pin = Pin(TRIGGER_PIN, Pin.OUT)
        sensor_echo_pin = Pin(ECHO_PIN, Pin.IN)

        # Simple check: toggle motor pin
        motor_pin.on()
        time.sleep(0.1)
        motor_pin.off()

        # If no exceptions, assume devices are connected
        print("Motor and sensor are connected.")
        return True
    except Exception as e:
        print("Device connection error:", e)
        return False

# Function to connect to Wi-Fi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to Wi-Fi...")
        sta_if.active(True)
        retry_count = 0
        sta_if.connect(SSID, PASSWORD)

        while not sta_if.isconnected():
            retry_count += 1
            if retry_count > WIFI_RETRY_LIMIT:
                print("Failed to connect to Wi-Fi after multiple attempts.")
                return False
            print(f"Retrying Wi-Fi connection... Attempt {retry_count}")
            time.sleep(2)

    print("Connected to Wi-Fi. Network configuration:", sta_if.ifconfig())
    return True

# Function to perform basic health checks
def perform_health_checks():
    print("Performing health checks...")

    # Check if Wi-Fi is connected
    wifi_connected = connect_wifi()
    if not wifi_connected:
        print("Wi-Fi check failed. Restarting...")
        time.sleep(2)
        reset()  # Restart ESP8266 if Wi-Fi fails

    # Check if devices are connected
    device_check = check_devices()
    if not device_check:
        print("Device check failed. Restarting...")
        time.sleep(2)
        reset()  # Restart ESP8266 if devices are not detected

    print("All health checks passed.")
    return True

# Main routine
def main():
    # Run health checks before executing main.py
    if perform_health_checks():
        print("Starting main application...")
        try:
            run()  # Call the run function from main.py directly
        except Exception as e:
            print("Error running main.py:", e)
            sys.print_exception(e)
            reset()  # Restart the ESP8266 in case of an error in main.py
    else:
        print("Health checks failed. Restarting...")
        reset()  # Restart if health checks fail

# Run the main function
main()


