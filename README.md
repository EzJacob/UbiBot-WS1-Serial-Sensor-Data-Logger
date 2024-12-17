# UbiBot-WS1-Serial-Sensor-Data-Logger
Python script for collecting and logging real-time sensor data from the UbiBot WS1 device into a CSV file for environmental monitoring and data acquisition.

## Features
- Communicates with the UbiBot WS1 device using a serial interface.
- Sends JSON commands to request sensor data.
- Logs sensor data (temperature, humidity, light, voltage) to a CSV file.
- Automatically appends a header if the CSV file doesn't exist.
- Collects data every 10 minutes (configurable).
- Handles device timeout and JSON parsing errors gracefully.

## Requirements
- Python 3.6 or higher
- Required Python libraries:
  - `pyserial`
  - `json`
  - `csv`
  - `datetime`
  - `os`
  - `time`

Install dependencies using:
```bash
pip install pyserial
```

## Usage
1. Connect your UbiBot WS1 device to your computer via a serial port.
2. Update the script's `com_port` variable with your device's COM port (e.g., `COM3`, `/dev/ttyUSB0`).
3. Run the script:
   ```bash
   python ubibot_ws1_data_logger.py
   ```
4. The sensor data will be logged to `sensor_data.csv`.

## Notes
- Ensure the UbiBot WS1 device is configured to the correct serial settings:
  - Baudrate: 115200
  - Data bits: 8
  - Parity: None
  - Stop bits: 1
- The script expects the device to respond with a JSON-formatted string containing sensor readings.

## Example Output
```
Timestamp: 2024-12-17 12:00:00, Temperature: 25.34°C, Humidity: 40.21%, Light: 125.5 lux, Voltage: 3.7 V
```
