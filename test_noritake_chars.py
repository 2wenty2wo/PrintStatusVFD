import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 19200, timeout=1)  # Adjust baud rate if needed

ser.write(b'\x0C')  # Clear screen
time.sleep(0.5)

ser.write(b'\x1F\x43\x00')  # Disable blinking cursor
time.sleep(0.1)

ser.write(b'Hello, Noritake!')
time.sleep(2)

ser.write(b'\x0C')  # Clear screen
ser.close()
