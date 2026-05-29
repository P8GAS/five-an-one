from fastapi import APIRouter
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats, teamdetails
from nba_api.library.http import NBAHTTP
from services.cache import get_cache, set_cache
import time

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

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.get("/search")
def search(q: str):
    all_teams = teams.get_teams()
    results = [
        t for t in all_teams
        if q.lower() in t["full_name"].lower()
    ]
    return results[:10]

@router.get("/{team_id}/info")
def get_info(team_id: int):
    cache_key = f"team_info_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    info = teamdetails.TeamDetails(team_id=team_id)
    data = info.get_data_frames()[0].to_dict(orient="records")[0]
    set_cache(cache_key, data)
    return data
