from dataclasses import dataclass
from typing import Any
import time

@dataclass
class Block:
    index: int
    timestamp: int
    data: Any
    prev_hash: str
    nonce: int
    hash: str
    difficulty: int

    @staticmethod
    def create(index: int, data: Any, prev_hash: str, difficulty: int) -> "Block":
        """Factory for initializing a new block before mining."""
        return Block(
            index=index,
            timestamp=int(time.time() * 1000),
            data=data,
            prev_hash=prev_hash,
            nonce=0,
            hash="",
            difficulty=difficulty,
        )
