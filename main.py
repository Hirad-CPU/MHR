from gpiozero import DigitalOutputDevice
import spidev
import time
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
HEIGHT = 320

def send_command(cmd):
    DC.off()
    CS.off()
    spi.writebytes([cmd])
    CS.on()

def send_data(data):
    if data is None:
        print("خطا: داده ورودی None است!")
        return
    
    DC.on()
    CS.off()
    chunk_size = 4096
    if isinstance(data, int):
        spi.writebytes([data])
    else:
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

    send_command(0xCB)
    send_data([0x39, 0x2C, 0x00, 0x34, 0x02])
    send_command(0xCF)
    send_data([0x00, 0xC1, 0x30])
    send_command(0xE8)
    send_data([0x85, 0x00, 0x78])
    send_command(0xEA)
    send_data([0x00, 0x00])
    send_command(0xED)
    send_data([0x64, 0x03, 0x12, 0x81])
    send_command(0xF7)
    send_data([0x20])
    send_command(0xC0)
    send_data([0x23])
    send_command(0xC1)
    send_data([0x10])
    send_command(0xC5)
    send_data([0x3E, 0x28])
    send_command(0xC7)
    send_data([0x86])
    send_command(0x36)
    send_data([0x48])  
    send_command(0x3A)
    send_data([0x55])  
    send_command(0xB1)
    send_data([0x00, 0x18])
    send_command(0xB6)
    send_data([0x08, 0x82, 0x27])
    send_command(0xF2)
    send_data([0x00])
    send_command(0x26)
    send_data([0x01])
    send_command(0xE0)
    send_data([0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E, 0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00])
    send_command(0xE1)
    send_data([0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31, 0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F])

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

def frame_to_rgb565(frame):
    if frame is None:
        print("خطا: فریم ورودی None است!")
        return []
    
    # تغییر اندازه فریم به ابعاد نمایشگر
    try:
        img = cv2.resize(frame, (WIDTH, HEIGHT))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # تبدیل BGR به RGB
    except Exception as e:
        print(f"خطا در پردازش تصویر: {e}")
        return []

    pixel_data = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = img[y, x]
            # اطمینان از اینکه مقادیر در محدوده 0-255 هستند
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # تبدیل به RGB565: 5 بیت قرمز، 6 بیت سبز، 5 بیت آبی
            r5 = (r >> 3) & 0x1F  # 5 بیت قرمز
            g6 = (g >> 2) & 0x3F  # 6 بیت سبز
            b5 = (b >> 3) & 0x1F  # 5 بیت آبی
            rgb565 = (r5 << 11) | (g6 << 5) | b5  # ترکیب بیت‌ها
            
            # تقسیم به دو بایت 8 بیتی
            pixel_data.append((rgb565 >> 8) & 0xFF)  # بایت بالایی
            pixel_data.append(rgb565 & 0xFF)          # بایت پایینی
    
    return pixel_data

def display_frame(frame):
    if frame is None:
        print("خطا: فریم ورودی None است!")
        return
    
    set_address_window(0, 0, WIDTH - 1, HEIGHT - 1)
    frame_data = frame_to_rgb565(frame)
    if not frame_data:  # بررسی اینکه داده خالی نباشد
        print("خطا: داده فریم خالی است!")
        return
    send_data(frame_data)

# --- تنظیمات تشخیص چهره ---
nameless = []
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(0)
today_date = datetime.today().strftime('%Y-%m-%d')
filename = f"{today_date}.txt"
print(f"فایل '{filename}' ایجاد شد.")

# مقداردهی اولیه نمایشگر
init_display()

# حلقه اصلی
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("خطا: فریم از دوربین دریافت نشد یا فریم None است!")
        time.sleep(0.1)  # تاخیر کوتاه برای جلوگیری از مصرف بی‌مورد CPU
        continue

    # تشخیص چهره
    face_locations, names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, names):
        if name not in nameless:
            name_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write = f"{name} is present at {name_time}\n"
            with open(filename, "a") as file:
                file.write(write)
            nameless.append(name)
        print(name)

    # نمایش فریم روی نمایشگر
    display_frame(frame)

    # نمایش فریم در پنجره OpenCV (اختیاری، برای دیباگ)
    cv2.imshow("Frame", frame)

    # خروج با کلید ESC
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
spi.close()
