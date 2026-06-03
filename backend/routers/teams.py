from fastapi import APIRouter
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamdetails, commonteamroster, boxscoretraditionalv2, teamgamelog, teamyearbyyearstats
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

@router.get("/")
def get_teams():
    cache_key = "all_teams"
    cached = get_cache(cache_key)
    if cached:
        return cached
    
    all_teams = teams.get_teams()

    set_cache(cache_key, all_teams)

    return sorted(all_teams, key=lambda x: x["full_name"])

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

@router.get("/{team_id}/starters")
def get_starters(team_id: int):
    cache_key = f"team_starters_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached   
    time.sleep(0.6)
    
    log = teamgamelog.TeamGameLog(team_id=team_id, season="2025-26")
    last_game_id = log.get_data_frames()[0].iloc[0]["Game_ID"] or log.get_data_frames()[2].iloc[0]["Game_ID"]

    time.sleep(0.6)

    box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=last_game_id)
    players = box.get_data_frames()[0]
    starters_id = players[(players["START_POSITION"] != "") & (players["TEAM_ID"] == team_id)]
    starters = [
        {"id": int(row["PLAYER_ID"]), "name": row["PLAYER_NAME"]}
        for _, row in starters_id.iterrows()
    ]

    set_cache(cache_key, starters)

    return starters

@router.get("/{team_id}/year_stats")
def get_year_stats(team_id: int, season: str = "2025-26"):
    cache_key = f"team_year_stats_{team_id}_{season}"
    cached = get_cache(cache_key)
    if cached:
        return cached
    time.sleep(0.6)

    stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
    df = stats.get_data_frames()[0]
    row = df[df["YEAR"] == season].to_dict(orient="records")
    if not row:
        return {"wins": 0, "losses": 0}
    data = {"wins": int(row[0]["WINS"]), "losses": int(row[0]["LOSSES"])}

    set_cache(cache_key, data)

    return data

@router.get("/{team_id}/card_info")
def get_card_info(team_id: int):
    cache_key = f"team_card_info_{team_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    data = {
        "info": get_info(team_id),
        "stats": get_year_stats(team_id),
        "starters": get_starters(team_id),
    }

    set_cache(cache_key, data)

    return data

