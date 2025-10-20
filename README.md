# Coin

A minimal blockchain implementation exploring how Bitcoin and proof-of-work systems function.

[Demo usage](./demo.gif)

## Overview

This project demonstrates the core concepts of blockchain technology:
- Proof of Work (PoW) mining
- Block validation
- Chain consensus
- Client-server architecture

## Requirements

Pure Python 3 - no external dependencies required. Uses only the standard library.

We use `uv` for package management, but you can run it directly with `python3` if preferred.

## Usage

**Start the server:**
```bash
python main.py server
```

**Mine and submit a block (in another terminal):**
```bash
python main.py client "Your transaction data here"
```

## How it Works

1. Server maintains a blockchain stored as a JSON list
2. Clients fetch the last block hash
3. Clients mine new blocks using SHA256 with configurable difficulty
4. Server validates:
   - Hash correctness (SHA256 of prev_hash + timestamp + data + nonce)
   - Difficulty requirement (leading zeros)
   - Chain continuity (prev_hash matches last block)
5. Valid blocks are appended to the chain

## Files

- `main.py` - Entry point (server/client modes)
- `server.py` - HTTP server with validation endpoints
- `client.py` - Mining client
- `pow.py` - Proof of Work algorithm + validation
- `schema.py` - Block data structure
- `db.py` - Simple key-value storage

## License

ISC

