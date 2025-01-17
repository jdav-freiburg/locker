DATE=$(date '+%Y-%m-%d %H:%M:%S')
echo  "${DATE}: starting fbcp" | systemd-cat -p info
fbcp
