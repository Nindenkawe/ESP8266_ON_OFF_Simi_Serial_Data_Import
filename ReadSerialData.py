import json
import serial
#import time

# Configure the serial port
port = '/dev/ttyACM0'  # Replace with your serial port
baudrate = 9600
timeout = 1  # Set a timeout for reading data

# Create a serial object
ser = serial.Serial(port, baudrate, timeout=timeout)

# Open the JSON file for writing
with open('on_street_doc.json', 'a') as file:
    while True:
        try:
            # Read a line from the serial port
            data = ser.readline()
            
            # Decode with error handling
            try:
                decoded_data = data.decode('utf-8').strip()  # Try UTF-8 first
            except UnicodeDecodeError:
                try:
                    decoded_data = data.decode('latin-1').strip()  # Try Latin-1 if UTF-8 fails
                except UnicodeDecodeError:
                    print(f"Decoding error: {data}")
                    continue  # Skip to the next iteration

            # Check if data was received
            if decoded_data:
                # Parse the data as JSON
                try:
                    data_json = json.loads(decoded_data)
                except json.JSONDecodeError:
                    print(f"Invalid JSON data received: {decoded_data}")
                    continue  # Skip to the next iteration

                # Write the JSON data to the file
                json.dump(data_json, file)
                file.write('\n')  # Add a newline for readability

        except serial.SerialException as e:
            print(f"Serial error: {e}")
            break  # Exit the loop on serial error

# Close the serial port
ser.close()
