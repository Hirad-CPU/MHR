import cv2
from simple_facerec import SimpleFacerec
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer

nameless = []
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = cv2.VideoCapture(1)

# مسیر فایل
file_path = "text.txt"

with open(file_path, "w") as file:
    while True:
        ret, frame = cap.read()
        face_location, name = sfr.detect_known_faces(frame)
        height, width, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 200), 2)
        
        for face_loc, name in zip(face_location, name):
            if name not in nameless:
                name_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                write = f"{name} is ready, in time {name_time}\n"
                file.write(write)
                file.flush()

                nameless.append(name)
            print(name)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:  # اگر کلید ESC فشرده شود، سرور HTTP اجرا می‌شود
            break

cap.release()
cv2.destroyAllWindows()

# راه‌اندازی سرور HTTP
class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/text.txt":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            with open(file_path, "r") as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found.")

print("Starting server...")
server_address = ("192.168.1.55", 8000)  # آدرس و پورت سرور
httpd = HTTPServer(server_address, CustomHandler)
print(f"Server running at http://{server_address[0]}:{server_address[1]}/text.txt")
httpd.serve_forever()
