# PrintStatusVFD

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/2wenty2wo/PrintStatusVFD.svg)](https://github.com/2wenty2wo/PrintStatusVFD/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/2wenty2wo/PrintStatusVFD.svg)](https://github.com/2wenty2wo/PrintStatusVFD/issues)
[![GitHub forks](https://img.shields.io/github/forks/2wenty2wo/PrintStatusVFD.svg)](https://github.com/2wenty2wo/PrintStatusVFD/network)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/2wenty2wo/PrintStatusVFD/graphs/commit-activity)

### Monitor your 3D printer's status on a VFD display using Home Assistant and Moonraker

_A lightweight Python script that updates a Posiflex PD-2800/320 VFD display with live 3D printer status from Home Assistant._

![Preview](preview.jpg)

## 🚀 Features
- ✅ **Live Print Status** — Displays `"Printing"`, `"Paused"`, `"Standby"`, etc.
- ✅ **Print Progress Bar** — Dynamic bar graph with percentage.
- ✅ **Time Remaining** — Converts seconds to a readable **HH:MM format**.
- ✅ **"Printer Ready" Mode** — Hides progress/time when idle.
- ✅ **Auto-Start on Boot** — Runs on Raspberry Pi via **systemd service**.
- ✅ **Easy Customization** — Change Home Assistant entity names via `config.py`.

---

## 🔧 What You Need
- 🖥️ **Raspberry Pi** (or any Linux system)
- 🔌 **Posiflex PD-2800/320 VFD display** (connected via USB)
- 🔄 **Home Assistant with Moonraker Plugin**
- 🐍 **Python 3 & Dependencies**

---

## 📥 Installation
### 1️⃣ Install Required Packages
Run these commands on your Raspberry Pi:
```bash
sudo apt update && sudo apt install -y python3 python3-pip
pip3 install requests
```

### 2️⃣ Clone This Repository
```bash
git clone https://github.com/YOUR_USERNAME/PrintStatusVFD.git
cd PrintStatusVFD
```

### 3️⃣ Configure Home Assistant API
Edit `config.py`:
```bash
nano config.py
```
Modify it to match your **Home Assistant API token & entities**:
```python
# Home Assistant Configuration
HA_URL = "http://homeassistant.local:8123/api/states"
HA_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"

# Home Assistant Entity IDs (Update based on your setup)
PRINTER_STATUS_ENTITY = "sensor.k1c_current_print_state"  # Printer state
PRINTER_PROGRESS_ENTITY = "sensor.k1c_progress"  # Print completion %
PRINTER_TIME_LEFT_ENTITY = "sensor.k1c_print_time_left"  # Time remaining in seconds
```
_Save and exit (`CTRL+X`, then `Y`, then `ENTER`)._

### 4️⃣ Test the Script
Run manually to check for errors:
```bash
python3 homeassistant_display.py
```
If everything works, press `CTRL+C` to stop.

---

## 🛠️ Setting Up Auto-Start on Boot
To ensure **PrintStatusVFD** starts automatically on reboot, create a **systemd service**.

### 1️⃣ Create a Service File
```bash
sudo nano /etc/systemd/system/vfd-display.service
```
Paste this inside:
```ini
[Unit]
Description=VFD Display Printer Status
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/PrintStatusVFD/homeassistant_display.py
WorkingDirectory=/home/pi/PrintStatusVFD
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
_Save and exit (`CTRL+X`, then `Y`, then `ENTER`)._

### 2️⃣ Enable & Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable vfd-display.service
sudo systemctl start vfd-display.service
```

### 3️⃣ Verify That It’s Running
```bash
sudo systemctl status vfd-display.service
```
You should see `"active (running)"` in green.

### 4️⃣ Reboot & Confirm It Works
```bash
sudo reboot
```
Check the display after rebooting!

---

## 🎯 Troubleshooting
### 🛑 The script doesn’t start on boot
- Check logs:
  ```bash
  journalctl -u vfd-display.service --no-pager | tail -50
  ```
- Restart the service manually:
  ```bash
  sudo systemctl restart vfd-display.service
  ```
- Ensure the script runs without errors:
  ```bash
  python3 homeassistant_display.py
  ```

### ⚠️ Display Shows "Printer Ready" Always
- Check if Home Assistant’s API is responding:
  ```bash
  curl -X GET -H "Authorization: Bearer YOUR_HA_LONG_LIVED_ACCESS_TOKEN"        -H "Content-Type: application/json"        http://homeassistant.local:8123/api/states
  ```
  If this fails, your Home Assistant API token may be incorrect.

### ⏳ The Time Remaining Seems Incorrect
- Ensure Home Assistant is providing the correct time in **seconds**.
- You can log the output by adding `print(time_left_sec)` inside `get_printer_status()`.

---

## 📝 Contributing
If you’d like to **improve PrintStatusVFD**, feel free to:
- 🐛 **Report bugs** via GitHub Issues.
- 💡 **Suggest features** by opening a discussion.
- 🔄 **Submit a pull request** if you add something awesome!

---

## 📜 License
This project is licensed under the **MIT License**—do whatever you want, just give credit! 😎  
