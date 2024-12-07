import time

import RPi.GPIO as GPIO

INPUT_PIN = 20
OUTPUT_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(5, False)


def open_bay():
    GPIO.output(OUTPUT_PIN, True)
    time.sleep(0.01)
    GPIO.output(OUTPUT_PIN, False)


def is_open():
   return GPIO.input(INPUT_PIN)
