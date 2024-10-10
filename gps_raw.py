import serial

port = "/dev/ttyAMA0"  # or /dev/ttyS0 if that's the correct port
ser = serial.Serial(port, baudrate=9600, timeout=1)

while True:
    try:
        # Read a line of raw data from the GPS
        raw_data = ser.readline().decode('ascii', errors='replace')
        if raw_data:
            print(f"Raw GPS Data: {raw_data}")
    except Exception as e:
        print(f"Error: {e}")
