#! /usr/bin/bash

# change to viable config directory and run program
# in a loop in case the program crashes
FJ_PATH="/home/pi/fjaelllada"
mkdir $FJ_PATH
cd $FJ_PATH || exit

while true
do
  seil-locker
done
