# وارد کردن کتابخانه‌ها و ماژول‌های مورد نیاز
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from machine import machine  # تابع ماشین از فایل machine

import requests  # برای ارسال درخواست HTTP
import os        # برای کار با فایل‌ها و مسیرها
from datetime import date  # برای گرفتن تاریخ امروز

# بخش try: برای دریافت فایل از سرور
try:
    # مشخص کردن آدرس سرور و پورت
    SERVER_IP = "192.168.1.55"
    PORT = 8000

    # گرفتن تاریخ امروز و ساخت نام فایل بر اساس آن
    today = date.today().strftime("%Y-%m-%d")
    FILENAME = f'{today}.txt'

    # مسیر ذخیره فایل دریافتی در سیستم کلاینت
    SAVE_PATH = "c:/hirad/random"

    # اگر مسیر ذخیره وجود نداشته باشد، ساخته می‌شود
    os.makedirs(SAVE_PATH, exist_ok=True)

    # ساخت آدرس کامل URL فایل
    url = f"http://{SERVER_IP}:{PORT}/{FILENAME}"
    
    # ارسال درخواست GET برای دریافت فایل
    response = requests.get(url)

    # نمایش وضعیت پاسخ
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # بررسی اینکه آیا دریافت فایل موفقیت‌آمیز بوده یا نه
    if response.status_code == 200:
        # ذخیره محتوای فایل در مسیر مشخص‌شده
        file_path = os.path.join(SAVE_PATH, FILENAME)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"✅ فایل '{FILENAME}' با موفقیت در مسیر '{file_path}' ذخیره شد.")
    else:
        print("❌ خطا در دریافت فایل!")

# اگر دریافت فایل با خطا مواجه شد، برنامه وارد بخش except می‌شود و رابط چت ساخته می‌شود
except:

    # کلاس حباب چت (نمایش پیام‌ها به شکل باکس در چت)
    class ChatBubble(QWidget):
        def __init__(self, message: str, is_sender: bool = False):
            """
            :param message: متن پیام
            :param is_sender: اگر True باشد، پیام از طرف کاربر است (راست‌چین)، در غیر این صورت چپ‌چین
            """
            super().__init__()
            self.message = message
            self.is_sender = is_sender
            self.setup_ui()

        # ساختار ظاهری حباب چت
        def setup_ui(self):
            layout = QHBoxLayout()
            layout.setContentsMargins(10, 5, 10, 5)
            self.setLayout(layout)

            # ساخت لیبل پیام
            self.label = QLabel(self.message)
            self.label.setWordWrap(True)
            self.label.setStyleSheet("""
                padding: 10px;
                border-radius: 10px;
                background-color: %s;
            """ % ("#DCF8C6" if self.is_sender else "#FFFFFF"))  # رنگ متفاوت برای کاربر و بات

            # تنظیم جایگاه پیام بسته به اینکه فرستنده کیست
            if self.is_sender:
                layout.addStretch()
                layout.addWidget(self.label)
            else:
                layout.addWidget(self.label)
                layout.addStretch()

    # کلاس پنجره اصلی چت
    class ChatWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("پنجره چت")  # عنوان پنجره
            self.setGeometry(100, 100, 400, 600)  # اندازه و موقعیت پنجره
            self.setup_ui()

        # ساخت اجزای رابط کاربری
        def setup_ui(self):
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(10, 10, 10, 10)
            main_layout.setSpacing(10)

            # قسمت نمایش پیام‌ها در ScrollArea برای اسکرول‌پذیر بودن
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setStyleSheet("border: none;")
            self.chat_container = QWidget()
            self.chat_layout = QVBoxLayout(self.chat_container)
            self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.scroll_area.setWidget(self.chat_container)
            main_layout.addWidget(self.scroll_area)

            # پیش‌نمایش چند پیام برای شروع (نمایش اولیه)
            bubble_user = ChatBubble("سلام خوبی", is_sender=True)
            self.chat_layout.addWidget(bubble_user)
            bubble_assistant = ChatBubble("سلام! خوبم، ممنون. تو چطوری؟", is_sender=False)
            self.chat_layout.addWidget(bubble_assistant)

            # قسمت ورودی پیام و دکمه ارسال
            input_layout = QHBoxLayout()
            self.input_field = QLineEdit()
            self.input_field.setPlaceholderText("پیام خود را بنویسید...")
            self.send_button = QPushButton("ارسال")
            self.send_button.clicked.connect(self.send_message)  # اتصال دکمه به تابع ارسال پیام

            input_layout.addWidget(self.input_field)
            input_layout.addWidget(self.send_button)
            main_layout.addLayout(input_layout)

        # تابع ارسال پیام
        def send_message(self):
            self.message = self.input_field.text().strip()
            if self.message:
                new_bubble = ChatBubble(self.message, is_sender=True)  # پیام کاربر به صورت حباب جدید
                self.chat_layout.addWidget(new_bubble)
                self.input_field.clear()
                self.bot()  # فراخوانی پاسخ بات
                # اسکرول خودکار به پایین برای نمایش آخرین پیام
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().maximum()
                )

        # تابع پاسخ بات
        def bot(self):
            self.name = machine(self.message)  # پردازش پیام با تابع machine
            print(self.name)
            chatbot_bubble = ChatBubble(self.name, is_sender=False)  # پاسخ بات به صورت حباب
            self.chat_layout.addWidget(chatbot_bubble)
            self.input_field.clear()
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
        def closeEvent(self, event):
            with open("CHECK.txt", "w") as file:
                file.write("")  # پاک‌سازی محتوای فایل
            event.accept()  # اجازه بده پنجره بسته بشه

    # اجرای برنامه
    name = "__main__"
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
    
