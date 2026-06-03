from fastapi import APIRouter
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo, playercareerstats
from nba_api.library.http import NBAHTTP
from services.cache import get_cache, set_cache
import time
import unicodedata

NBAHTTP.headers = {
    "Host": "stats.nba.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Connection": "keep-alive",
}

def normalize(name: str) -> str:
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8').lower()

router = APIRouter(prefix="/players", tags=["Players"])

@router.get("/search")
def search(q: str):
    all_players = players.get_players()
    results = [
        p for p in all_players
        if normalize(q) in normalize(p["full_name"])
    ]
    return results[:10]

@router.get("/{player_id}/info")
def get_info(player_id: int):
    cache_key = f"player_info_{player_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    data = info.get_data_frames()[0].to_dict(orient="records")[0]
    set_cache(cache_key, data)
    return data

@router.get("/{player_id}/stats")
def get_stats(player_id: int, per_mode: str = "PerGame"):
    cache_key = f"player_stats_{player_id}_{per_mode}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    log = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36=per_mode)
    data = { 
        "regular_season": log.get_data_frames()[0].to_dict(orient="records"),
        "playoffs": log.get_data_frames()[2].to_dict(orient="records")
    }
    set_cache(cache_key, data)
    return data

@router.get("/{player_id}/card_info")
def get_card_info(player_id: int):
    cache_key = f"player_card_info_{player_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    data = {
        "info": get_info(player_id),
        "stats": get_stats(player_id, per_mode="PerGame")
    }
    set_cache(cache_key, data)
    return data
