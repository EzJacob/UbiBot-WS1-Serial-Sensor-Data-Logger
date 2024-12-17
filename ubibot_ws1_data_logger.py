import serial
import json
import time
import csv
from datetime import datetime
import os

# Set the correct COM port (e.g., 'COM3', 'COM4', etc.)
com_port = 'COM3'  # Replace with your actual COM port
baud_rate = 115200  # Updated baud rate according to your requirements

# Initialize the serial connection with the correct settings
ser = serial.Serial(
    com_port,
    baudrate=baud_rate,
    bytesize=serial.EIGHTBITS,  # Data bits: 8
    parity=serial.PARITY_NONE,  # Parity: None
    stopbits=serial.STOPBITS_ONE,  # Stop bits: 1
    timeout=1
)

# CSV file setup
csv_file = "sensor_data.csv"

# Check if the header has already been written by checking if the first row contains headers
def check_if_header_exists(file_path, header):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            first_row = next(reader, None)  # Read the first row
            if first_row == header:
                return True
    return False

# Define the header
header = ["Timestamp", "Temperature (C)", "Humidity (%)", "Light (lux)", "Voltage (V)"]

# Check if the header exists, if not, write it
if not check_if_header_exists(csv_file, header):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

# Function to send the command and save the data
def collect_sensor_data():
    command = {"command": "CheckSensors"}
    command_str = json.dumps(command) + '\n'  # Convert to JSON and add newline
    ser.write(command_str.encode('utf-8'))    # Send the command to the device

    # Wait and read the response, giving the device more time if necessary
    start_time = time.time()
    response = ""

    while True:
        if ser.in_waiting > 0:
            response += ser.read(ser.in_waiting).decode('utf-8')  # Read the available data
        if '\n' in response:  # Check if a complete response (usually ends with newline) has been received
            break
        if time.time() - start_time > 10:  # Timeout after 10 seconds if no response
            print("Timeout: No response from device.")
            return
        time.sleep(0.1)  # Sleep briefly to avoid hogging CPU while waiting

    # Parse the response and save it to CSV
    try:
        data = json.loads(response)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        temperature = round(data.get("temp_val", 0), 2)
        humidity = round(data.get("humi_val", 0), 2)
        light = round(data.get("light_val", 0), 2)
        voltage = round(data.get("power_vol_val", 0), 2)

        # Print the collected data
        print(f"Timestamp: {timestamp}, Temperature: {temperature}°C, Humidity: {humidity}%, Light: {light} lux, Voltage: {voltage} V")

        # Save the data to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity, light, voltage])

    except json.JSONDecodeError:
        print("Failed to parse response as JSON.")

# Loop to run the command every 10 minutes
try:
    while True:
        collect_sensor_data()
        print("Waiting for the next reading in 10 minutes...")
        time.sleep(600)  # Wait for 10 minutes (600 seconds)
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()  # Close the serial connection when the script stops
