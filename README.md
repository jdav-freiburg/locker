# Raspberry PI interface

for accessing the hardware locker using registered RFID cards.

## Installation

Install display
```sh
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod +x LCD35-show
./LCD35-show
sudo apt install ./libacsccid1_1.1.8-1~bpo10+1_armhf.deb
sudo apt install python3-pyscard pcscd
```

Replace the end of `/boot/config.txt` by:
```
# Additional overlays and parameters are documented /boot/overlays/README

dtoverlay=waveshare35a
framebuffer_width=480
framebuffer_height=320
framebuffer_depth=16
hdmi_force_hotplug=1
disable_overscan=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=960 640 60 6 0 0 0
hdmi_drive=1
```
(480x320 seems to end up wrong if set as cvt)

Create venv and install requirements:
```sh
python -m venv --system-site-packages venv
pip install pyotp qrcode
```
Copy `.xsession` over.

