import requests
import os
from datetime import datetime

# آدرس سرور و فایل موردنظر
SERVER_IP = "192.168.1.55"
PORT = 8000
FILENAME = f'{datetime.today().strftime('%Y-%m-%d')}.txt'  # نام فایل موردنظر
SAVE_PATH = "c:/hirad/random"  # مسیر ذخیره فایل در کلاینت

# اطمینان از وجود مسیر ذخیره‌سازی
os.makedirs(SAVE_PATH, exist_ok=True)

# دریافت فایل از سرور
url = f"http://{SERVER_IP}:{PORT}/{FILENAME}"
response = requests.get(url)

print(f"Response Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# بررسی موفقیت دانلود
if response.status_code == 200:
    file_path = os.path.join(SAVE_PATH, FILENAME)  # مسیر نهایی فایل
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"✅ فایل '{FILENAME}' با موفقیت در مسیر '{file_path}' ذخیره شد.")
else:
    print("❌ خطا در دریافت فایل!")