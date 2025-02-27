import cv2
from simple_facerec import SimpleFacerec
from datetime import datetime
from gpiozero import DigitalOutputDevice
import spidev
import time
from PIL import Image

# تنظیم پایه‌های GPIO برای نمایشگر LCD
CS = DigitalOutputDevice(22)
DC = DigitalOutputDevice(17)
RST = DigitalOutputDevice(27)

# مقداردهی اولیه SPI
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
HEIGHT = 320

def send_command(cmd):
    DC.off()
    CS.off()
    spi.writebytes([cmd])
    CS.on()

def send_data(data):
    DC.on()
    CS.off()
    if isinstance(data, int):
        spi.writebytes([data])
    else:
        chunk_size = 4096
        for i in range(0, len(data), chunk_size):
            spi.writebytes(data[i:i+chunk_size])
    CS.on()

def init_display():
    RST.off()
    time.sleep(0.1)
    RST.on()
    time.sleep(0.1)

    send_command(ILI9341_SWRESET)
    time.sleep(0.12)

    send_command(ILI9341_SLPOUT)
    time.sleep(0.12)

    send_command(ILI9341_DISPON)
    time.sleep(0.12)

def set_address_window(x0, y0, x1, y1):
    send_command(ILI9341_CASET)
    send_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])

    send_command(ILI9341_PASET)
    send_data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])

    send_command(ILI9341_RAMWR)

def convert_image_to_rgb565(image):
    img = img.resize((WIDTH, HEIGHT))
    img = img.convert('RGB')

    pixel_data = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = img.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            pixel_data.append(rgb565 >> 8)
            pixel_data.append(rgb565 & 0xFF)
    return pixel_data

def display_image_on_lcd(frame):
    set_address_window(0, 0, WIDTH - 1, HEIGHT - 1)
    image_data = convert_image_to_rgb565(frame)
    send_data(image_data)

nameless = []
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(1)

# مسیر فایل
file_path = "text.txt"

with open(file_path, "w") as file:
    init_display()  # مقداردهی اولیه نمایشگر LCD

    while True:
        ret, frame = cap.read()
        face_location, name = sfr.detect_known_faces(frame)
        height, width, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 200), 2)

        for face_loc, name in zip(face_location, name):
            if name not in nameless:
                name_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                write = f"{name} is ready, in time {name_time}\n"
                file.write(write)
                file.flush()

                nameless.append(name)
            print(name)

        # نمایش تصویر روی LCD به جای نمایش در OpenCV
        display_image_on_lcd(frame)

        key = cv2.waitKey(1)
        if key == 27:  # اگر کلید ESC فشرده شود، برنامه متوقف می‌شود
            break

cap.release()
cv2.destroyAllWindows()
