import os
import sqlite3
from typing import Optional, Any

_DB_PATH = os.path.join(os.path.dirname(__file__), "kv.sqlite3")


def _ensure_db() -> None:
    with sqlite3.connect(_DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value BLOB)"
        )
        conn.commit()


def _ensure_db_ready(func):
    def wrapper(*args, **kwargs):
        _ensure_db()
        return func(*args, **kwargs)
    return wrapper


@_ensure_db_ready
def set(key: str, value: Any) -> None:
    with sqlite3.connect(_DB_PATH) as conn:
        conn.execute(
            "INSERT INTO kv(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )
        conn.commit()


@_ensure_db_ready
def get(key: str) -> Optional[str]:
    with sqlite3.connect(_DB_PATH) as conn:
        cur = conn.execute("SELECT value FROM kv WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else None