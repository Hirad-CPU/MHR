mport http.server
import socketserver
import os

def httpp():
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "CHECK.txt" :
                self.path = "CHECK.txt"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            else :
                self.send_error(404, "File not found")

    PORT = 8000

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server started at http://192.168.1.55:{PORT}")
        httpd.serve_forever()
