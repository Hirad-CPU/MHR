import time
import os
import subprocess

scripts = ['nain.py', 'finger.py', 'httpp.py']
processes = []

# اجرای اسکریپت‌ها و ذخیره پروسه‌ها
for script in scripts:
    process = subprocess.Popen(['python3', script], cwd="/home/np/Lcd/Face-recognition/face_recognition")
    processes.append(process)

print("All scripts started. Keeping Asly.py alive...")
while True:
    # چک کردن اینکه اسکریپت‌ها هنوز زنده‌ان یا نه
    for process in processes:
        if process.poll() is not None:  # اگه یه اسکریپت تموم شده باشه
            print(f"Script {process.args[1]} stopped. Restarting...")
            processes.remove(process)
            new_process = subprocess.Popen(process.args, cwd="/home/np/Lcd/Face-recognition/face_recognition")
            processes.append(new_process)
    time.sleep(60)  # هر ۶۰ ثانیه چک کن
