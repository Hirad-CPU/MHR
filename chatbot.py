import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from machine import machine

import requests
import os
from datetime import date

try:
    # آدرس سرور و فایل موردنظر
    SERVER_IP = "192.168.1.55"
    PORT = 8000
    today=date.today().strftime("%Y-%m-%d")
    FILENAME = f'{today}.txt'  # نام فایل موردنظر
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

except:

    class ChatBubble(QWidget):
        def __init__(self, message: str, is_sender: bool = False):
            """
            :param message: متن پیام
            :param is_sender: True اگر پیام از کاربر (راست چین) و False برای پیام‌های دریافتی (چپ چین)
            """
            super().__init__()
            self.message = message
            self.is_sender = is_sender
            self.setup_ui()

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
            """ % ("#DCF8C6" if self.is_sender else "#FFFFFF"))

            # چیدمان پیام بر اساس فرستنده
            if self.is_sender:
                layout.addStretch()
                layout.addWidget(self.label)
            else:
                layout.addWidget(self.label)
                layout.addStretch()

    class ChatWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("پنجره چت")
            self.setGeometry(100, 100, 400, 600)
            self.setup_ui()

        def setup_ui(self):
            # ویجت مرکزی و چیدمان اصلی
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setContentsMargins(10, 10, 10, 10)
            main_layout.setSpacing(10)

            # قسمت نمایش پیام‌ها در یک ScrollArea
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setStyleSheet("border: none;")
            self.chat_container = QWidget()
            self.chat_layout = QVBoxLayout(self.chat_container)
            self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.scroll_area.setWidget(self.chat_container)
            main_layout.addWidget(self.scroll_area)

            # پیش‌نمایش چند پیام (مثلاً همانگونه که در تصویر دیده می‌شود)
            # پیام کاربر
            bubble_user = ChatBubble("سلام خوبی", is_sender=True)
            self.chat_layout.addWidget(bubble_user)
            # پیام دریافت شده (مثلاً از طرف دستیار)
            bubble_assistant = ChatBubble("سلام! خوبم، ممنون. تو چطوری؟", is_sender=False)
            self.chat_layout.addWidget(bubble_assistant)

            # قسمت ورودی پیام
            input_layout = QHBoxLayout()
            self.input_field = QLineEdit()
            self.input_field.setPlaceholderText("پیام خود را بنویسید...")
            self.send_button = QPushButton("ارسال")
            self.send_button.clicked.connect(self.send_message)

            input_layout.addWidget(self.input_field)
            input_layout.addWidget(self.send_button)
            main_layout.addLayout(input_layout)

        def send_message(self):
            self.message = self.input_field.text().strip()
            if self.message:
                new_bubble = ChatBubble(self.message, is_sender=True)
                self.chat_layout.addWidget(new_bubble)
                self.input_field.clear()
                self.bot()
                # اسکرول خودکار به پایین
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().maximum()
                )

            
        def bot(self):
                
                self.name=machine(self.message)
                print(self.name)
                chatbot_bubble = ChatBubble(self.name, is_sender=False)
                self.chat_layout.addWidget(chatbot_bubble)
                self.input_field.clear()
                # اسکرول خودکار به پایین
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().maximum()
                )
                

    name = "__main__"
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
