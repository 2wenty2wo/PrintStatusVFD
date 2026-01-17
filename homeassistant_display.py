import serial
import requests
import time
import config  # Load API Token & URL from config.py
import signal
import sys

# Home Assistant API Config
HA_URL = config.HA_URL
HA_TOKEN = config.HA_TOKEN
HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}

# Home Assistant Entity Config
PRINTER_STATUS_ENTITY = config.PRINTER_STATUS_ENTITY
PRINTER_PROGRESS_ENTITY = config.PRINTER_PROGRESS_ENTITY
PRINTER_TIME_LEFT_ENTITY = config.PRINTER_TIME_LEFT_ENTITY
PRINTER_DURATION_ENTITY = config.PRINTER_DURATION_ENTITY  # New entity for completed print time

# Function to initialize the serial connection
def initialize_serial():
    while True:
        try:
            return serial.Serial('/dev/ttyACM0', 19200, timeout=1)
        except serial.SerialException:
            print("VFD display not found. Retrying in 2 seconds...")
            time.sleep(2)

# Initialize serial connection
ser = initialize_serial()

# Store last displayed values to prevent unnecessary updates
last_display = ""
last_valid_duration = ""  # Default to empty if no valid duration exists yet

# Function to clear the screen when script exits
def clear_screen_and_exit(signal_received=None, frame=None):
    """Clears the display before exiting."""
    ser.write(b'\x0C')  # Clear screen command
    ser.close()
    sys.exit(0)

# Handle script exit (CTRL+C or termination)
signal.signal(signal.SIGINT, clear_screen_and_exit)
signal.signal(signal.SIGTERM, clear_screen_and_exit)

# Function to Fetch Data from Home Assistant
def get_printer_status():
    global last_valid_duration
    try:
        response = requests.get(HA_URL, headers=HEADERS)
        data = response.json()

        # Extract values safely, ensuring no None or missing keys
        status = next((item.get("state", "Unknown") for item in data if item.get("entity_id") == PRINTER_STATUS_ENTITY), "Unknown").lower()
        progress = next((item.get("state", "0") for item in data if item.get("entity_id") == PRINTER_PROGRESS_ENTITY), "0")
        time_left_sec = next((item.get("state", "0") for item in data if item.get("entity_id") == PRINTER_TIME_LEFT_ENTITY), "0")
        duration_sec = next((item.get("state", "0") for item in data if item.get("entity_id") == PRINTER_DURATION_ENTITY), "0")

        # Convert progress safely
        try:
            progress = int(float(progress))  # Handle float as a string
        except ValueError:
            progress = 0

        # Convert time from seconds to HH:MM format
        try:
            time_left_sec = int(float(time_left_sec))  # Ensure time is an integer
            duration_sec = int(float(duration_sec))  # Ensure time is an integer
            hours = time_left_sec // 3600
            minutes = (time_left_sec % 3600) // 60

            duration_hours = duration_sec // 3600
            duration_minutes = (duration_sec % 3600) // 60

            # Always show minutes, only show hours if needed
            time_remaining = f"{hours}h {minutes:02}m" if hours > 0 else (f"{minutes}m" if minutes > 0 else "")
            duration_display = f"{duration_hours}h {duration_minutes:02}m" if duration_hours > 0 else (f"{duration_minutes}m" if duration_minutes > 0 else "")
        except ValueError:
            time_remaining = ""
            duration_display = ""

        # Preserve last known valid print duration if Home Assistant resets it to 0
        if status == "printing" and duration_sec > 0:
            last_valid_duration = duration_display
        elif status == "complete" and duration_sec == 0:
            duration_display = last_valid_duration  # Use last valid duration

        # Map statuses to improved display messages
        status_map = {
            "printing": "Printing",
            "complete": "Print Done",
            "standby": "Idle",
            "cancelled": "Print Canceled"
        }
        display_status = status_map.get(status, "Unknown")

        # If print is complete, show total print time instead of time remaining
        if status == "complete":
            return display_status, 100, duration_display

        # Hide progress and time if not printing
        if status not in ["printing"]:
            return display_status, None, ""

        return display_status, progress, time_remaining

    except Exception as e:
        return "Error", None, ""

# Function to Generate ASCII Progress Bar Dynamically
def generate_progress_bar(progress, available_width):
    """Generate a progress bar that fits in the available space"""
    if progress is None:
        return " " * available_width  # Blank bar when idle
    filled_blocks = round((progress / 100) * available_width)
    return "#" * filled_blocks + "-" * (available_width - filled_blocks)

# Main Loop to Update Display Smoothly
while True:
    try:
        # Check if serial connection is still active
        if not ser.is_open:
            print("VFD disconnected! Attempting to reconnect...")
            ser = initialize_serial()

        # Fetch new data
        status, progress, time_remaining = get_printer_status()

        # **Format percentage only if printing or completed**
        perc_str = f"{progress}% " if progress is not None else "    "  # Blank when idle

        # **Calculate progress bar width dynamically**
        progress_bar_width = 18 - (len(perc_str))  # Available space for progress bar
        progress_bar = generate_progress_bar(progress, progress_bar_width)

        # Construct the full two-line display text
        line1 = f"{status:<14}{time_remaining:>6}"  # Status left, time remaining right (or print duration when complete)
        line2 = f"[{progress_bar}] {perc_str}" if progress is not None else " " * 20  # Progress bar left, percentage right

        # Ensure full overwrite by forcing each line to be exactly 20 characters
        display_text = f"{line1[:20]}{line2[:20]}"

        # Only update the screen if something has changed
        if display_text != last_display:
            last_display = display_text
            ser.write(b'\x0C')  # Clear screen
            time.sleep(0.1)
            ser.write(display_text.encode())  # Write new text

        time.sleep(1)  # Update every second

    except KeyboardInterrupt:
        clear_screen_and_exit()
    except Exception as e:
        print(f"Error: {e}")  # Print error for debugging but don't exit loop
