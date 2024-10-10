sudo gpsd -N -F /var/run/gpsd.sock /tmp/gpspipe

python3 fake_gps_data.py
