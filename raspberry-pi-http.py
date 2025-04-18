import http.server
import socketserver
import socket
import threading
import time

# دریافت آدرس IP فعلی سیستم (برای نمایش لینک سرور)
def get_ip():
    return socket.gethostbyname(socket.gethostname())

# تابعی برای توقف خودکار سرور بعد از مدت زمان مشخص (بر حسب ثانیه)
def stop_server(httpd, duration):
    time.sleep(duration)  # صبر می‌کنه تا زمان مشخص‌شده بگذره
    print("\nServer stopped automatically after 10 minutes.")
    httpd.shutdown()  # خاموش کردن سرور
    print("stop reading")  # پیام کمکی برای دیباگ یا آگاهی

# تابع اصلی راه‌اندازی سرور HTTP ساده
def httpp():
    PORT = 8000  # پورت محلی که سرور روی اون اجرا میشه
    Handler = http.server.SimpleHTTPRequestHandler  # کنترل‌کننده‌ی پیش‌فرض برای پاسخ به درخواست‌ها

    # ایجاد و راه‌اندازی سرور با استفاده از socketserver
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        ip = get_ip()  # گرفتن IP دستگاه برای نمایش آدرس کامل
        print(f"Server started at http://{ip}:{PORT}")

      
        try:
            httpd.serve_forever()  # اجرای بی‌پایان سرور تا زمان توقف دستی یا خودکار
        except KeyboardInterrupt:
            # در صورتی که کاربر با Ctrl+C بخواد سرور رو متوقف کنه
            print("\nServer stopped manually.")
            httpd.server_close()  # بستن دستی سرور
