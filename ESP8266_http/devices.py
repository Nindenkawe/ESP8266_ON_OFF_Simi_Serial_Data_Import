# devices.py
import machine
import time

class MotorControl:
    def __init__(self, motor_pin):
        """Initializes motor control on the given pin."""
        self.motor = machine.Pin(motor_pin, machine.Pin.OUT)
        self.angle = 0  # Initial angle set to 0

    def rotate_to_angle(self, target_angle):
        """Rotates the motor to a specific target angle (North, East, South, West)."""
        while self.angle != target_angle:
            self.motor.on()
            time.sleep(0.5)  # Adjust based on motor speed and angle change
            self.motor.off()
            
            # Update the angle in 90-degree increments
            self.angle = (self.angle + 90) % 360

            # Brief delay to simulate motor turning
            time.sleep(1)

    def stop(self):
        """Stops the motor."""
        self.motor.off()

    def get_angle(self):
        """Returns the current angle of the motor."""
        return self.angle

    def get_direction(self):
        """Returns the current direction based on the angle."""
        directions = {
            0: "North",
            90: "East",
            180: "South",
            270: "West"
        }
        return directions.get(self.angle, "Unknown")

class ProximitySensor:
    def __init__(self, trigger_pin, echo_pin, threshold=50):
        """Initializes the HC-SR04 ultrasonic sensor (threshold: 50cm)."""
        self.trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)
        self.threshold = threshold

    def measure_distance(self):
        """Measures the distance using the HC-SR04 sensor."""
        self.trigger.off()
        time.sleep_us(5)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()

        pulse_time = machine.time_pulse_us(self.echo, 1, 30000)  # 30ms timeout
        distance_cm = (pulse_time / 2) / 29.1  # Convert time to distance in cm
        return distance_cm

    def is_object_near(self):
        """Checks if an object is within the threshold distance."""
        distance = self.measure_distance()
        return distance <= self.threshold, distance


