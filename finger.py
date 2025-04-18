import time
import board
import adafruit_fingerprint
import serial
from datetime import datetime


# تنظیم ارتباط سریال با سنسور اثر انگشت از طریق پورت UART
uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################

# تابعی برای گرفتن اثر انگشت و بررسی اینکه آیا تطابق دارد یا نه
def get_fingerprint():
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass  # تا زمانی که تصویری از انگشت گرفته نشود، منتظر می‌ماند

    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False  # تبدیل تصویر به الگو ناموفق بود

    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False  # جستجو برای تطابق ناموفق بود

    return True  # تطابق موفقیت‌آمیز بود


# نسخه‌ی دقیق‌تر تابع بالا برای نمایش خطاهای ممکن
def get_fingerprint_detail():
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="")
    i = finger.finger_fast_search()
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# ثبت یک اثر انگشت جدید در سیستم
def enroll_finger():
    # ثبت دو تصویر از یک انگشت برای ساخت مدل کامل
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")  # منتظر بودن برای قرار دادن انگشت
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            print("we have a problem")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    # خواندن بزرگ‌ترین عدد ID از فایل
    with open("fingerprints.txt", "r", encoding="utf-8") as file:
        numbers = [int(line.split()[0]) for line in file if line.split()[0].isdigit()]
    max_number = max(numbers)
    new_number = max_number + 1

    # خواندن نام مربوطه از فایل CHECK.txt
    with open("CHECK.txt", "r", encoding="utf-8") as name_file:
        lines = name_file.readlines()
        if len(lines) > 1:
            name = lines[1].strip()
        else:
            name = "Unknown"

# ذخیره ID جدید همراه با نام در فایل fingerprints.txt
with open("fingerprints.txt", "a", encoding="utf-8") as file:
    # بررسی اینکه آیا فایل خالی است یا خیر
    file.seek(0, 2)  # رفتن به انتهای فایل
    if file.tell() > 0:  # اگر فایل خالی نیست، یک خط جدید اضافه کن
        file.write("\n")
    file.write(f"{new_number} {name}")
    location = new_number

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

##################################################

# تبدیل فایل متنی به دیکشنری برای دسترسی سریع به نام‌ها بر اساس ID
def load_fingerprint_data(filename="fingerprints.txt"):
    fingerprint_dict = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # نادیده گرفتن خطوط خالی
                    continue
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    fingerprint_id, name = parts
                    fingerprint_dict[int(fingerprint_id)] = name
    except FileNotFoundError:
        print("Error: File not found!")
    return fingerprint_dict

# بررسی وجود مقدار خاص در فایل، و اگر نبود، اضافه کردن آن
def check_and_store(value, filename="data.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
        lines = []

    if str(value) not in lines:
        with open(filename, "a") as file:
            file.write(str(value) + "\n")
        print(f'"{value}" به فایل اضافه شد.')
    else:
        print(f'"{value}" قبلاً در فایل وجود دارد.')

# بارگذاری نام‌ها در شروع برنامه
fingerprint_names = load_fingerprint_data()


# حذف تمام اثر انگشت‌ها از سنسور و فایل مربوطه
def delete_all_fingerprints():
    print("Deleting all fingerprints from sensor...")
    for location in range(1, 1000):
        if finger.delete_model(location) == adafruit_fingerprint.OK:
            print(f"Fingerprint {location} deleted from sensor.")
        else:
            print(f"Failed to delete fingerprint {location} from sensor.")

    try:
        with open("fingerprints.txt", "w", encoding="utf-8") as file:
            file.truncate(0)
        print("All fingerprints removed from fingerprints.txt.")
    except FileNotFoundError:
        print("Error: fingerprints.txt not found!")

# حذف یک اثر انگشت خاص بر اساس نام موجود در CHECK.txt
def delete_fingerprint_by_name():
    try:
        with open("CHECK.txt", "r", encoding="utf-8") as name_file:
            lines = name_file.readlines()
            if len(lines) > 1:
                name_to_delete = lines[1].strip()
            else:
                print("Error: No valid name found in CHECK.txt")
                return
    except FileNotFoundError:
        print("Error: CHECK.txt not found!")
        return

    fingerprint_entries = []
    fingerprint_id = None

    try:
        with open("fingerprints.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    id_number, stored_name = parts
                    if stored_name == name_to_delete:
                        fingerprint_id = int(id_number)
                    else:
                        fingerprint_entries.append(line.strip())
    except FileNotFoundError:
        print("Error: fingerprints.txt not found!")
        return

    if fingerprint_id is None:
        print(f"Name '{name_to_delete}' not found in fingerprints.txt!")
        return

    print(f"Deleting fingerprint {fingerprint_id} from sensor...")
    if finger.delete_model(fingerprint_id) == adafruit_fingerprint.OK:
        print(f"Fingerprint {fingerprint_id} deleted from sensor.")
    else:
        print(f"Failed to delete fingerprint {fingerprint_id} from sensor.")

    try:
        with open("fingerprints.txt", "w", encoding="utf-8") as file:
            for entry in fingerprint_entries:
                file.write(entry + "\n")
        print(f"Entry '{fingerprint_id} {name_to_delete}' removed from fingerprints.txt.")
    except FileNotFoundError:
        print("Error: Unable to update fingerprints.txt!")

##################################################

# حلقه‌ی اصلی برنامه که مرتباً بررسی می‌کند چه کاری باید انجام شود
while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")

    print("Fingerprint templates:", finger.templates)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("----------------")

    # خواندن دستورات از فایل CHECK.txt
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = file.read().splitlines()
        time.sleep(13)  # تاخیر برای آماده‌سازی

    if 2 in file_data1:
        enroll_finger()
        time.sleep(2)

    if 3 in file_data1:
        delete_all_fingerprints()
        time.sleep(2)

    if 5 in file_data1:
        delete_fingerprint_by_name()
        time.sleep(2)

    # بررسی وجود اثر انگشت تطابق‌یافته
    if get_fingerprint():
    user_id = finger.finger_id
    confidence = finger.confidence
    if user_id in fingerprint_names:
        name = fingerprint_names[user_id]
        print("Detected:", name, "with confidence", confidence)

        # گرفتن تاریخ امروز و ساختن نام فایل
        today = datetime.now().strftime("%Y-%m-%d") 
        filename = f"{today}.txt"

        # ذخیره نام اگر قبلاً ثبت نشده
        check_and_store(name, filename)
    else:
        print("Detected fingerprint with unknown ID.")
else:
    print("Detected unknown fingerprint.")
