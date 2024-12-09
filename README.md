# Raspberry PI interface

for accessing the hardware locker using registered RFID cards.

## Hardware

See the [depot-oben-eda](depot-oben-eda) folder for kicad Drawings
Open the project file with [KiCad](https://www.kicad.org/) (used version is 8) to view the schematic and board design
for the small transistor board for opening the solenoid.

The pinout for the Raspberry Pi is as follows (BCM numbering!):

Pull up `SWITCH` to turn on the solenoid, don't hold too long because it tends to overheat quite fast. (<= 500 ms)
`CHECK` is high-z when the locker is open and GND when it is closed. To prevent floating state
pull up the GPIO pin to which `CHECK` is connected.

| Board Pin | RaspberryPi Pin |
| :-------- | :-------------- |
| SWITCH    | GPIO21          |
| CHECK     | GPIO20          |
| GND       | GND             |

For pinout info see [pinout.xyz/](https://pinout.xyz/)



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

## Software
See the [Software Docs](software/README.md) for details.
