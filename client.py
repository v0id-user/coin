import json
import urllib.request
import urllib.error
from dataclasses import asdict
from pow import mine
from schema import Block


def get_last_hash(server_url: str) -> str:
    """
    Fetch the last block hash from the server.
    
    Args:
        server_url: Base URL of the blockchain server
        
    Returns:
        The hash of the last block in the chain
    """
    try:
        response = urllib.request.urlopen(f"{server_url}/last")
        data = json.loads(response.read().decode('utf-8'))
        return data["last_hash"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No blocks found on server")
            return "0" * 64  # Return genesis hash
        raise


def submit_block(server_url: str, block: Block) -> dict:
    """
    Submit a mined block to the server for validation.
    
    Args:
        server_url: Base URL of the blockchain server
        block: The Block object to submit
        
    Returns:
        Server response as a dictionary
    """
    # Convert Block dataclass to dictionary
    block_dict = asdict(block)
    block_json = json.dumps(block_dict).encode('utf-8')
    
    # Create POST request
    req = urllib.request.Request(
        f"{server_url}/coin",
        data=block_json,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_response = json.loads(e.read().decode('utf-8'))
        return error_response


def mine_and_submit(server_url: str, data: str) -> None:
    """
    Complete flow: get last hash, mine new block, and submit to server.
    
    Args:
        server_url: Base URL of the blockchain server
        data: Transaction data or payload for the new block
    """
    print(f"Fetching last block hash from {server_url}...")
    last_hash = get_last_hash(server_url)
    print(f"Last hash: {last_hash[:16]}...")
    
    print(f"\nMining new block with data: '{data}'")
    block_hash, nonce, mining_time, block = mine(last_hash, data)
    
    print(f"✓ Block mined!")
    print(f"  Hash: {block_hash}")
    print(f"  Nonce: {nonce}")
    print(f"  Time: {mining_time:.2f}s")
    
    print(f"\nSubmitting block to server...")
    response = submit_block(server_url, block)
    
    if response.get("success"):
        print(f"✓ Block accepted by server!")
        print(f"  Hash: {response.get('hash')}")
    else:
        print(f"✗ Block rejected by server")
        print(f"  Error: {response.get('error')}")


def startClient():
    server_url = "http://localhost:42122"
    
    print("=== Blockchain Client ===\n")
    
    data = "Sample transaction data"
    
    mine_and_submit(server_url, data)