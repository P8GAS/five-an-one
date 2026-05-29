from fastapi import APIRouter
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamdetails, commonteamroster
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

@router.get("/{team_id}/logo")
def get_logo(team_id: int):
    cache_key = f"team_logo_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    url = f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
    set_cache(cache_key, {"url": url})
    return {"url": url}

@router.get("/{team_id}/roster")
def get_roster(team_id: int):
    cache_key = f"team_roster_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    roster = commonteamroster.CommonTeamRoster(team_id=team_id)
    roster = roster.get_data_frames()[0].to_dict(orient="records")
    set_cache(cache_key, roster)
    return roster

@router.get("/{team_id}/card_info")
def get_card_info(team_id: int):
    cache_key = f"team_card_info_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)
    data = {
        "logo": get_logo(team_id),
        "info": get_info(team_id),
        "roster": get_roster(team_id)
    }
    set_cache(cache_key, data)
    return data