# cache/simple_cache.py
import hashlib
import json
import os
from typing import Any, Optional

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _key_for(*parts) -> str:
    h = hashlib.sha256(("||".join(map(str, parts))).encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.json")

def get_cached(*parts) -> Optional[Any]:
    path = _key_for(*parts)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def set_cached(value: Any, *parts):
    path = _key_for(*parts)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(value, f)
    except Exception:
        pass
