import json
import os
import time

CACHE_DIR = "cache/"
CACHE_DURATION = 60 * 60 * 24  # 24 heures en secondes

def get_cache(key: str):
    path = f"{CACHE_DIR}{key}.json"

    if not os.path.exists(path):
        return None

    age = time.time() - os.path.getmtime(path)
    if age > CACHE_DURATION:
        return None

    with open(path, "r") as f:
        return json.load(f)

def set_cache(key: str, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = f"{CACHE_DIR}{key}.json"

    with open(path, "w") as f:
        json.dump(data, f)