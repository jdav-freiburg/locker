import os
import time

from fjaelllada.env import DEBUG_SIMULATE_OUTPUT

if DEBUG_SIMULATE_OUTPUT:
    class GPIO:
        @staticmethod
        def setmode(a): pass
        @staticmethod
        def setup(a, b, pull_up_down=0): pass
        @staticmethod
        def output(a, b): pass
        @staticmethod
        def input(a): pass
        PUD_UP = 0
        BCM = 0
        OUT = 0
        IN = 0
else:
    import RPi.GPIO as GPIO

INPUT_PIN = int(os.environ.get("INPUT_PIN", "20"))
OUTPUT_PIN = int(os.environ.get("OUTPUT_PIN", "21"))

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(OUTPUT_PIN, False)


def open_bay():
    GPIO.output(OUTPUT_PIN, True)
    time.sleep(0.01)
    GPIO.output(OUTPUT_PIN, False)


def is_open():
   return GPIO.input(INPUT_PIN)
