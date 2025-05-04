import sys
import os
import time
import threading
import requests
from datetime import date

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from machine import machine  # فرض بر این است که تابع machine در فایل جدا است

# تابع اجرای دریافت فایل در پس‌زمینه
def download_file_loop():
    SERVER_IP = "192.168.1.55"
    PORT = 8000
    SAVE_PATH = "c:/hirad/random"
    os.makedirs(SAVE_PATH, exist_ok=True)

    while True:
        try:
            today = date.today().strftime("%Y-%m-%d")
            FILENAME = f'{today}.txt'
            url = f"http://{SERVER_IP}:{PORT}/{FILENAME}"
            response = requests.get(url)

            print(f"[دانلود فایل] وضعیت: {response.status_code}")
            if response.status_code == 200:
                file_path = os.path.join(SAVE_PATH, FILENAME)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"✅ فایل '{FILENAME}' با موفقیت ذخیره شد.")
            else:
                print("⚠️ فایل موجود نیست یا پاسخ مناسب دریافت نشد.")

        except Exception as e:
            print(f"❌ خطا در اتصال به سرور یا دریافت فایل: {e}")

        time.sleep(10)

# کلاس نمایش پیام‌ها به صورت حباب چت
class ChatBubble(QWidget):
    def __init__(self, message: str, is_sender: bool = False):
        super().__init__()
        self.message = message
        self.is_sender = is_sender
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        self.setLayout(layout)

        self.label = QLabel(self.message)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("""
            padding: 10px;
            border-radius: 10px;
            background-color: %s;
        """ % ("#DCF8C6" if self.is_sender else "#FFFFFF"))

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
        self.setWindowTitle("پنجره چت")
        self.setGeometry(100, 100, 400, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area)

        bubble_user = ChatBubble("سلام خوبی", is_sender=True)
        self.chat_layout.addWidget(bubble_user)
        bubble_assistant = ChatBubble("سلام! خوبم، ممنون. تو چطوری؟", is_sender=False)
        self.chat_layout.addWidget(bubble_assistant)

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
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )

    def bot(self):
        self.name = machine(self.message)
        print(self.name)
        chatbot_bubble = ChatBubble(self.name, is_sender=False)
        self.chat_layout.addWidget(chatbot_bubble)
        self.input_field.clear()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        with open("CHECK.txt", "w") as file:
            file.write("")
        event.accept()

# اجرای برنامه
#if __name__ == "__main__":
# اجرای نخ پس‌زمینه برای دانلود فایل بدون ارور
threading.Thread(target=download_file_loop, daemon=True).start()

# اجرای رابط گرافیکی
app = QApplication(sys.argv)
window = ChatWindow()
window.show()
sys.exit(app.exec())
