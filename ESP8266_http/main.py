import time
import json
import socket
import uasyncio as asyncio
from devices import MotorControl, ProximitySensor

# Pin definitions
MOTOR_PIN = 5
TRIGGER_PIN = 16
ECHO_PIN = 0

# Create objects for motor and sensor
motor = MotorControl(MOTOR_PIN)
sensor = ProximitySensor(TRIGGER_PIN, ECHO_PIN)

# Function to handle incoming HTTP requests
def handle_request(conn):
    try:
        request = conn.recv(1024)  # Receive the request
        print("Request:", request)  # Print the raw request (for debugging)

        # Get sensor data
        object_near, distance = sensor.is_object_near()
        angle = motor.get_angle()

        # Create a JSON response
        response = {
            "direction": motor.get_direction(),
            "angle": angle,
            "distance_cm": distance,
            "object_near": object_near
        }

        # Build the HTTP response headers and body
        http_response = "HTTP/1.1 200 OK\r\n"
        http_response += "Content-Type: application/json\r\n\r\n"
        http_response += json.dumps(response)

        # Send the response
        conn.sendall(http_response.encode('utf-8'))
        conn.close()

    except Exception as e:
        print("Error handling request:", e)
        conn.close()

# Start a simple HTTP server
async def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print("Listening on", addr)

    while True:
        conn, addr = server_socket.accept()
        print('Connection from', addr)
        handle_request(conn)

# Main loop to control motor and sensor readings
async def main_loop():
    directions = {
        "North": 0,
        "East": 90,
        "South": 180,
        "West": 270
    }

    current_direction = "North"
    current_angle = directions[current_direction]

    while True:
        # Rotate motor to the current direction
        print(f"Rotating motor to {current_direction}")
        motor.rotate_to_angle(target_angle=current_angle)

        # Wait for motor to settle
        await asyncio.sleep(1)

        # Move to the next direction
        next_index = (list(directions).index(current_direction) + 1) % len(directions)
        current_direction = list(directions)[next_index]
        current_angle = directions[current_direction]

        # Wait 10 seconds before rotating to the next direction
        await asyncio.sleep(10)

# Run the main loop and HTTP server concurrently
async def run():
    await asyncio.gather(start_server(), main_loop())

# Start the asyncio event loop
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print("Error in main loop:", e)


