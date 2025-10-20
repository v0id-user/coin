from dataclasses import dataclass
from typing import Any
import time

@dataclass
class Block:
    timestamp: int
    data: Any
    prev_hash: str
    nonce: int
    hash: str
    difficulty: int

    @staticmethod
    def create(data: Any, prev_hash: str, hash: str, difficulty: int, timestamp: int = None, nonce: int = 0) -> "Block":
        """Factory for initializing a new block before mining."""
        if timestamp is None:
            timestamp = int(time.time() * 1000)
        return Block(
            timestamp=timestamp,
            data=data,
            prev_hash=prev_hash,
            nonce=nonce,
            hash=hash,
            difficulty=difficulty,
        )
