# Fjaelllada deployment guide

### seil_locker

1. Flash a clean Raspbian Image to an SD Card (Raspberry Pi OS 32-bit) as
   we are using an older Pi which doesn't support a 64-bit OS. 
   If you're using the RPi Imager, set options for wifi and ssh directly to
   avoid the need to plug in a monitor and peripherals.
   Change the password!

2. Install required apt packages:  
`apt install git vim libacsccid1 pcscd libpcsclite-dev python3 python3-pip python3-pyscard python3-pyqt5`

3. Install display drivers from the waveshare git repo:
```sh
cd /tmp
git clone https://github.com/waveshare/LCD-show.git
cd LCD-show/
chmod u+x LCD35-show
./LCD35-show
```

4. Append the following options to `/boot/config.txt`. This is required for proper display initialization:
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

5. Reboot, the display should display a login screen when booted
6. Copy the built wheel of fjaelllada. See [Build instructions](software/README.md#building)
7. Install the wheel with `pip install <wheelfile>`. 
    >If it throws compile errors or takes very long check the versions of >`python3-pyqt5` and `python3-pyscard` with `apt show <pkg-name>` and make sure >these versions match
    >those defined in [pyproject.toml](software/pyproject.toml) exactly.
8. create a subfolder under `~` where fjaelllada will put it's logs and db files.
9. create an `.env` file in this directory. Adapt all env variables from [README](software/README.md)
10. copy the [.xsession](.xsession) file to `~`. 
11. reboot, the pi should show the UI after rebooting
12. Add an admin user
13. Login with that admin user to add cards for accessing the locker