import time
import board
import adafruit_fingerprint
import serial

uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
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

def enroll_finger():
    """Take a 2 finger images and template it, then store in 'location'"""
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
                print(".", end="")
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


    # خواندن بزرگ‌ترین عدد از فایل fingerprints.txt
    with open("fingerprints.txt", "r", encoding="utf-8") as file:
        numbers = [int(line.split()[0]) for line in file if line.split()[0].isdigit()]

    max_number = max(numbers)
    new_number = max_number + 1

    # خواندن یک نام از فایل دیگر
    with open("CHECK.txt", "r", encoding="utf-8") as name_file:
        lines = name_file.readlines()  # خواندن تمام خطوط
        if len(lines) > 1:  # بررسی اینکه حداقل دو خط وجود دارد
            name = lines[1].strip()  # گرفتن دومین خط و حذف فاصله‌های اضافی
        else:
            name = "Unknown"  # اگر خط دوم نبود، مقدار پیش‌فرض


    # اضافه کردن مقدار جدید به فایل fingerprints.txt
    with open("fingerprints.txt", "a", encoding="utf-8") as file:
        file.write(f"\n{new_number} {name}")  # اضافه کردن مقدار جدید در خط جدید
    location=new_number
    


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

    

# تابعی برای خواندن فایل و تبدیل به دیکشنری
def load_fingerprint_data(filename="fingerprints.txt"):
    fingerprint_dict = {}  # دیکشنری برای نگه‌داری داده‌ها
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(maxsplit=1)  # جدا کردن ID و نام
                if len(parts) == 2:  # اطمینان از اینکه داده‌ها درست باشند
                    fingerprint_id, name = parts
                    fingerprint_dict[int(fingerprint_id)] = name  # ذخیره در دیکشنری
    except FileNotFoundError:
        print("Error: File not found!")
    return fingerprint_dict
def check_and_store(value, filename="data.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()  # خواندن تمام خطوط و حذف \n
    except FileNotFoundError:
        lines = []

    if str(value) not in lines:
        with open(filename, "a") as file:
            file.write(str(value) + "\n")
        print(f'"{value}" به فایل اضافه شد.')
    else:
        print(f'"{value}" قبلاً در فایل وجود دارد.')

# بارگذاری نام‌ها از فایل
fingerprint_names = load_fingerprint_data()

def delete_all_fingerprints():
    """حذف تمام اثر انگشت‌ها از سنسور و فایل"""
    # حذف تمامی اثر انگشت‌ها از سنسور
    print("Deleting all fingerprints from sensor...")
    for location in range(1, 1000):  # فرض می‌کنیم که حداکثر 500 اثر انگشت می‌تواند ذخیره شود
        if finger.delete_model(location) == adafruit_fingerprint.OK:
            print(f"Fingerprint {location} deleted from sensor.")
        else:
            print(f"Failed to delete fingerprint {location} from sensor.")

    # حذف تمام داده‌ها از فایل fingerprints.txt
    try:
        with open("fingerprints.txt", "w", encoding="utf-8") as file:
            file.truncate(0)  # محتویات فایل را پاک می‌کند
        print("All fingerprints removed from fingerprints.txt.")
    except FileNotFoundError:
        print("Error: fingerprints.txt not found!")


while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates:", finger.templates)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")    
    print("----------------")
    with open("CHECK.txt", "r", encoding="utf-8") as file:
        file_data1 = file.read().splitlines()
        time.sleep(13)
    if 2 in file_data1:
        enroll_finger()
        time.sleep(2)
    if 3 in file_data1:
        delete_all_fingerprints()


    # تابع بررسی اثر انگشت
    if get_fingerprint():
        user_id = finger.finger_id
        confidence = finger.confidence

        # بررسی اینکه ID در دیکشنری وجود دارد یا نه
        if user_id in fingerprint_names:
            print("Detected:", fingerprint_names[user_id], "with confidence", confidence)
            # تست کد
        check_and_store("test_value")

    else:
        print("Detected unknown fingerprint with confidence", confidence)
