import time
import os
import random

def generate_nmea_sentence():
    # Generate random latitude and longitude
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    
    # NMEA sentence format: $GNRMC
    nmea_sentence = f"$GNRMC,{int(time.time())},{'A'},{latitude:.6f},{'N'},{longitude:.6f},{'E'},0.00,0.00,{time.strftime('%d%m%y')},"
    print(nmea_sentence)
    return nmea_sentence

def main():
    gpsd_socket = '/tmp/gpspipe'  # GPSD socket for communication
    os.system(f"sudo gpsd -N -F /var/run/gpsd.sock {gpsd_socket}")

    with open(gpsd_socket, 'w') as gps_socket:
        while True:
            nmea = generate_nmea_sentence()
            gps_socket.write(nmea + '\n')
            gps_socket.flush()
            time.sleep(1)  # Update every second

if __name__ == '__main__':
    main()
