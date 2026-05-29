import json
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_DURATION = 60 * 60 * 24  # 24 heures

def get_cache(key: str):
    path = os.path.join(CACHE_DIR, f"{key}.json")

    if not os.path.exists(path):
        return None

    age = time.time() - os.path.getmtime(path)
    if age > CACHE_DURATION:
        os.remove(path)
        return None

    with open(path, "r") as f:
        return json.load(f)

def set_cache(key: str, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    with open(path, "w") as f:
        json.dump(data, f)