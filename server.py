from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import db
from schema import Block
from pow import validate_block

# https://docs.python.org/3/library/http.server.html
class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello, World!')
        elif self.path == "/last":
            blockchain_json = db.get("blockchain")
            if blockchain_json:
                blockchain = json.loads(blockchain_json)
                last_hash = blockchain[-1]["hash"]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"last_hash": last_hash}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No blocks found"}).encode())

    def do_POST(self):
        if self.path == "/coin":
            # Read the full request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                # Parse JSON to Block object
                block_dict = json.loads(body.decode('utf-8'))
                block = Block(**block_dict)
                
                # Load blockchain from database
                blockchain_json = db.get("blockchain")
                if blockchain_json:
                    blockchain = json.loads(blockchain_json)
                else:
                    blockchain = []
                
                # Validate prev_hash matches the last block in the chain
                if blockchain:
                    last_block = blockchain[-1]
                    if block.prev_hash != last_block["hash"]:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "Invalid prev_hash"}).encode())
                        return
                else:
                    # First block after genesis must reference genesis
                    if block.prev_hash != "0" * 64:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "Invalid prev_hash for first block"}).encode())
                        return
                
                # Validate PoW (strict: hash correctness + difficulty)
                if not validate_block(block):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid PoW"}).encode())
                    return
                
                # Append block to blockchain and save
                blockchain.append(block_dict)
                db.set("blockchain", json.dumps(blockchain))
                
                # Success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "hash": block.hash}).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        

def startServer():
    # Initialize genesis block if blockchain doesn't exist
    blockchain_json = db.get("blockchain")
    if not blockchain_json:
        genesis_block = {
            "timestamp": 0,
            "data": "Genesis Block",
            "prev_hash": "0" * 64,
            "nonce": 0,
            "hash": "0" * 64,
            "difficulty": 0
        }
        db.set("blockchain", json.dumps([genesis_block]))
        print("Genesis block initialized")
    
    with HTTPServer(("0.0.0.0", 42122), RequestHandler) as http:
        print("Server Ready at http://localhost:42122")
        http.serve_forever()

if __name__ == "__main__":
    startServer()
