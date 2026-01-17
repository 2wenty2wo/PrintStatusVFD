import serial
import time

# Connect to Posiflex VFD
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Clear screen
ser.write(b'\x0C')  # Clear screen
time.sleep(0.1)

# Print first line normally
ser.write(b'Creality K1C')

# Force the second line by sending a carriage return + line feed
ser.write(b'\r\nStatus: Printing')

# Close connection
ser.close()
