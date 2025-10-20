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
    def create(data: Any, prev_hash: str, hash: str, difficulty: int) -> "Block":
        """Factory for initializing a new block before mining."""
        return Block(
            timestamp=int(time.time() * 1000),
            data=data,
            prev_hash=prev_hash,
            nonce=0,
            hash=hash,
            difficulty=difficulty,
        )
