import time
import board
import adafruit_fingerprint
import serial

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

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

def enroll_finger(location):
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
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
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

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 1000) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-1000: "))
        except ValueError:
            pass
    return i
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

while True:
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates:", finger.templates)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("----------------")
    
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
