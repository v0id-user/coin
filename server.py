from http.server import HTTPServer, SimpleHTTPRequestHandler
import sqlite3

# https://docs.python.org/3/library/http.server.html
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello, World!')
        

def startServer():
    with HTTPServer(("0.0.0.0", 42122), RequestHandler) as http:
        print("Server Ready at http://localhost:42122")
        http.serve_forever()

if __name__ == "__main__":
    startServer()
