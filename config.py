# Home Assistant Configuration
HA_URL = "http://homeassistant.local:8123/api/states"
HA_TOKEN = "HOME-ASSISTANT-TOKEN-HERE"

# Home Assistant Entity IDs (Customize these based on your setup)
PRINTER_STATUS_ENTITY = "sensor.k1c_current_print_state"  # Status: printing, paused, standby, etc.
PRINTER_PROGRESS_ENTITY = "sensor.k1c_progress"  # Print progress percentage
PRINTER_TIME_LEFT_ENTITY = "sensor.k1c_print_time_left"  # Time remaining in seconds
PRINTER_DURATION_ENTITY = "sensor.k1c_print_duration" # Print duration