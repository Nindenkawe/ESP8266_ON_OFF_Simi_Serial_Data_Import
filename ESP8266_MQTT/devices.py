from machine import Pin, time_pulse_us
import time  # Import the time module

class Sensor:
    def __init__(self, pin):
        """Initializes a generic digital sensor on the given pin."""
        self.pin = Pin(pin, Pin.IN)

    def read_value(self):
        """Reads and returns the current state of the sensor (0 or 1)."""
        return self.pin.value()

class Motor:
    def __init__(self, pin):
        """Initializes motor control on the given pin."""
        self.pin = Pin(pin, Pin.OUT)

    def on(self):
        """Turns the motor on."""
        self.pin.on()

    def off(self):
        """Turns the motor off."""
        self.pin.off()

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        """Initializes the HC-SR04 ultrasonic sensor."""
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def measure_distance(self):
        """Measures the distance using the HC-SR04 sensor."""
        self.trigger.off()
        time.sleep_us(5)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()

        pulse_time = time_pulse_us(self.echo, 1, 30000)  # 30ms timeout
        distance_cm = (pulse_time / 2) / 29.1  # Convert time to distance in cm
        return distance_cm
