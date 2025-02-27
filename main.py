from gpiozero import DigitalOutputDevice
import spidev
import time
from PIL import Image
import cv2
from simple_facerec import SimpleFacerec
from datetime import datetime

# --- تنظیمات نمایشگر ILI9341 ---
CS = DigitalOutputDevice(22)  # Chip Select
DC = DigitalOutputDevice(17)  # Data/Command
RST = DigitalOutputDevice(27) # Reset

spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 40000000  

# دستورات ILI9341
ILI9341_SWRESET = 0x01
ILI9341_SLPOUT  = 0x11
ILI9341_DISPON  = 0x29
ILI9341_CASET   = 0x2A
ILI9341_PASET   = 0x2B
ILI9341_RAMWR   = 0x2C

WIDTH = 240
HEIGHT = 
