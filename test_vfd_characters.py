import serial
import time

# Initialize the VFD Display
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Function to clear the screen
def clear_screen():
    ser.write(b'\x0C')  # Clear screen command
    time.sleep(0.5)

# Set of characters to test
test_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~????????"

# Split into multiple lines if needed
line_length = 20  # Max characters per line

# Test each character
for i in range(0, len(test_chars), line_length):
    clear_screen()
    ser.write(test_chars[i:i+line_length].encode())  # Display 20 characters at a time
    time.sleep(2)  # Wait 2 seconds before testing next set

# Clear screen after test
clear_screen()
ser.close()
