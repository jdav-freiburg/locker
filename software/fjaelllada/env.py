import os
from dotenv import load_dotenv

load_dotenv()

DEBUG_SIMULATE_CARD_READER = bool(os.environ.get("DEBUG_SIMULATE_CARD_READER", ""))
DEBUG_SIMULATE_OUTPUT = bool(os.environ.get("DEBUG_SIMULATE_OUTPUT", ""))

SCREEN_RESOLUTION_WIDTH = int(os.environ.get("SCREEN_RESOLUTION_WIDTH", "480"))
SCREEN_RESOLUTION_HEIGHT = int(os.environ.get("SCREEN_RESOLUTION_HEIGHT", "320"))

TOTP_ISSUER = os.environ.get("TOTP_ISSUER", "jdav-locker-v1")

INPUT_PIN = int(os.environ.get("INPUT_PIN", "21"))
OUTPUT_PIN = int(os.environ.get("OUTPUT_PIN", "20"))
