import requests
import os
from datetime import date

# آدرس سرور و فایل موردنظر
SERVER_IP = "192.168.1.55"
PORT = 8000
today = date.today().strftime("%Y-%m-%d")
FILENAME = f'{today}.txt'  # نام فایل موردنظر
SAVE_PATH = "c:/hirad/random"  # مسیر ذخیره فایل در کلاینت

# اطمینان از وجود مسیر ذخیره‌سازی
os.makedirs(SAVE_PATH, exist_ok=True)

# دریافت فایل از سرور
url = f"http://{SERVER_IP}:{PORT}/{FILENAME}"

try:
    response = requests.get(url, timeout=5)  # محدودیت زمانی برای جلوگیری از هنگ‌کردن
    if response.status_code == 200:  # بررسی موفقیت‌آمیز بودن درخواست
        file_path = os.path.join(SAVE_PATH, FILENAME)  # مسیر نهایی فایل
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"✅ فایل '{FILENAME}' با موفقیت در مسیر '{file_path}' ذخیره شد.")
    else:
        print("❌ فایل موردنظر در سرور موجود نیست.")
except requests.ConnectionError:
    pass  # در صورت عدم دسترسی به سرور، هیچ‌کاری انجام نمی‌شود
