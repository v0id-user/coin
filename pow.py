"""
Proof of Work (PoW) Mining Module

This module implements the core Proof of Work algorithm for cryptocurrency mining.
Clients must successfully mine blocks using computational work before they can 
register their claims on the blockchain network.

The mining process involves finding a nonce value that, when combined with the
previous block hash, timestamp, and data, produces a hash that meets the network's
difficulty requirements (starts with a specific number of leading zeros).

Algorithm:
    blockHash = SHA256(prevHash + timestamp + data + nonce)

Attributes:
    difficulty (int): The number of leading zeros required in the hash.
                     Higher values increase mining difficulty.

References:
    - https://en.wikipedia.org/wiki/Proof_of_work
    - Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)

Version:
    1.0.0
"""
from hashlib import sha256
import time

from schema import Block

difficulty = 5  # means hash must start with "000..."


def mine(prev_hash: str, data: str, nonce: int = 0) -> tuple[str, int, float, Block]:
    """
    Mine a new block by finding a valid nonce that satisfies the difficulty requirement.
    
    This function implements the core Proof of Work algorithm by iteratively trying
    different nonce values until a hash is found that starts with the required number
    of leading zeros (as defined by the global difficulty variable).
    
    The mining process combines the previous block hash, current timestamp, block data,
    and nonce to create a SHA256 hash. The function continues until a valid hash is
    found that meets the network's difficulty requirements.
    
    Args:
        prev_hash (str): The hash of the previous block in the blockchain.
        data (str): The transaction data or payload to be included in this block.
        nonce (int, optional): Starting nonce value for mining. Defaults to 0.
    
    Returns:
        tuple[str, int, float]: A tuple containing:
            - block_hash (str): The SHA256 hash of the mined block
            - final_nonce (int): The nonce value that produced the valid hash
            - mining_time (float): Time taken to mine the block in seconds
    
    Raises:
        ValueError: If prev_hash or data are empty strings.
    
    Example:
        >>> prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        >>> data = "Transaction data here"
        >>> block_hash, nonce, time_taken = mine(prev_hash, data)
        >>> print(f"Mined block: {block_hash[:16]}... with nonce: {nonce}")
        Mined block: 0000a1b2c3d4e5f6... with nonce: 12345
    
    Note:
        Mining time increases exponentially with difficulty. Higher difficulty values
        require significantly more computational work and time to find valid hashes.
    """
    if not prev_hash or not data:
        raise ValueError("prev_hash and data cannot be empty")
    
    timestamp = time.time()
    start_time = time.time()
    
    # Convert timestamp to string for hashing
    timestamp_str = str(int(timestamp))
    
    # Target prefix based on difficulty (e.g., "0000" for difficulty=4)
    target_prefix = "0" * difficulty
    
    while True:
        # Create the block data string: prevHash + timestamp + data + nonce
        block_data = prev_hash + timestamp_str + data + str(nonce)
        
        # Calculate SHA256 hash
        block_hash = sha256(block_data.encode('utf-8')).hexdigest()
        
        # Check if hash meets difficulty requirement
        if block_hash.startswith(target_prefix):
            mining_time = time.time() - start_time
            block = Block.create(data, prev_hash, block_hash, difficulty)
            return block_hash, nonce, mining_time, block
        
        # Increment nonce and try again
        nonce += 1