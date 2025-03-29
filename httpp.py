import http.server
import socketserver
import socket
import threading
import time

def get_ip():
    return socket.gethostbyname(socket.gethostname())

def stop_server(httpd, duration):
    time.sleep(duration)
    print("\nServer stopped automatically after 10 minutes.")
    httpd.shutdown()
    print("stop reading")

def httpp():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        ip = get_ip()
        print(f"Server started at http://{ip}:{PORT}")

        # اجرای تایمر برای متوقف کردن سرور بعد از  10 ثانیه
        threading.Thread(target=stop_server, args=(httpd, 10), daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped manually.")
            httpd.server_close()
