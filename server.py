from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        super().__init__(request, client_address, server)

    
    def handle(self) -> None:

        return super().handle()

def startServer():
    with HTTPServer(("0.0.0.0", 42122), RequestHandler) as server:
        print("Server Ready at http://localhost:42122")
        server.serve_forever()
