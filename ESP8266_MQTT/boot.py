import network
import time

# Wi-Fi credentials
SSID = "Wutang_LAN-2G"
PASSWORD = "..,123456"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Wi-Fi connected:", wlan.ifconfig())

# Connect to Wi-Fi on boot
connect_wifi()

# Now execute main.py
import main
