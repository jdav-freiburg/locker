# Raspberry PI interface

for accessing the hardware locker using registered RFID cards.

## Installation

Install display
```sh
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod +x LCD35-show
./LCD35-show
sudo vim /boot/config.txt
# For Raspberry Zero W, comment out
# hdmi_cvt=480 320 60 6 0 0 0
# and set:
# hdmi_cvt=640 420 60 1 0 0 0

sudo apt install ./libacsccid1_1.1.8-1~bpo10+1_armhf.deb
python -m venv --system-site-packages venv
pip install pyotp qrcode
sudo apt install python3-pyscard pcscd

```

Copy `.xsession` over.
