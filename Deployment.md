# Fjaelllada deployment guide

### seil_locker
> The following guide is for Debian Bookworm. Other versions might differ!

1. Flash a clean Raspbian Image to an SD Card (Raspberry Pi OS 32-bit) as
   we are using an older Pi which doesn't support a 64-bit OS. 
   If you're using the RPi Imager, set options for wifi and ssh directly to
   avoid the need to plug in a monitor and peripherals.
   Change the password!  
   If updates are available, update the packages

2. Install required apt packages & reboot:
`apt install curl git vim cmake unzip libacsccid1 pcscd libraspberrypi-dev raspberrypi-kernel-headers libpcsclite-dev python3 python3-pip python3-pyscard python3-pyqt5 xserver-xorg-input-evdev xinput-calibrator xserver-xorg-video-fbturbo`

3.  Download and compile drivers and overlays from waveshare:
```bash
wget https://files.waveshare.com/upload/1/1e/Waveshare35a.zip
unzip ./Waveshare35a.zip
sudo cp waveshare35a.dtbo /boot/overlays/
wget https://files.waveshare.com/upload/1/1e/Rpi-fbcp.zip
unzip ./Rpi-fbcp.zip
cd rpi-fbcp/
mkdir build
cd build
cmake ..
make
sudo install fbcp /usr/local/bin/fbcp
cd ~
rm -r rpi-fbcp
rm waveshare35a.dtbo
```

4. Comment out the following lines in `/boot/firmware/config.txt`:
```bash
# Enable DRM VC4 V3D driver  
#dtoverlay=vc4-kms-v3d  
#max_framebuffers=2
```

5. Append the following options to `/boot/firmware/config.txt`. This is required for proper display initialization:
```
dtparam=spi=on  
dtoverlay=waveshare35a  
hdmi_force_hotplug=1  
max_usb_current=1  
hdmi_group=2  
hdmi_mode=87  
hdmi_cvt 640 480 60 6 0 0 0  
hdmi_drive=2  
display_rotate=0
```


6. copy `99-calibration.conf` and `99-fbturbo.conf` to `/usr/share/X11/xorg.conf.d`
7. Run `mv 10-evdev.conf 45-evdev.conf`
8. Append `Option "InvertX" "true"` to the last catchall block
9. Go to the `raspi-config` menu and change the following settings:
	- Display -> screen blanking -> off
	- System -> AutoLogin -> Desktop Autologin
10. Reboot, the display should display a login screen when booted
11. Copy the built wheel of fjaelllada. See [Build instructions](software/README.md#building)
12. Install the wheel with `pip install --user --break-system-packages <wheelfile>`. 
>Check that the verisons of the APT python packages match those defined in  [pyproject.toml](software/pyproject.toml) exactly. It may crash your packages otherwise
>If it throws compile errors or takes very long check the versions of `python3-pyqt5` and
>`python3-pyscard` with `apt show <pkg-name>` and 
> make sure these versions match those defined exactly. 
13. create `~/fjaelllada`
14. create an `.env` file in this directory. Adapt all env variables from [README](software/README.md)
15. Copy `autostart` to `~/.config/lxsession/LXDE-pi/autostart`
16. Copy `start-fjaelllada.sh` and `start_fbcp.sh` to `/home/pi/fjaelllada`
17. Copy `start_fbcp.service` to `~/.config/systemd/user/fjaelllada` and run `systemctl --user enable fbcp.service`
18. reboot, the pi should show fjaelllada's UI after rebooting
19. Add an admin user
20. Login with that admin user to add cards for accessing the locker
