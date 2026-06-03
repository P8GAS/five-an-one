from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import players, teams
from contextlib import asynccontextmanager
from requests.exceptions import ReadTimeout
import asyncio

async def preheat_cache():
    from nba_api.stats.static import teams as nba_teams
    from routers.teams import get_card_info
    from services.cache import get_cache

    all_teams = nba_teams.get_teams()
    to_load = [t for t in all_teams if not get_cache(f"team_card_info_{t['id']}")]

    if not to_load:
        print(">>> Preheat: tout est déjà en cache ✓", flush=True)
        return

    print(f">>> Preheat: {len(to_load)}/{len(all_teams)} équipes à charger", flush=True)
    for i, team in enumerate(to_load):
        try:
            get_card_info(team["id"])
            print(f">>> [{i+1}/{len(to_load)}] {team['full_name']} ✓", flush=True)
        except Exception as e:
            print(f">>> [{i+1}/{len(to_load)}] {team['full_name']} ✗", flush=True)
        await asyncio.sleep(2)

    print(">>> Preheat terminé", flush=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(preheat_cache())
    yield

app = FastAPI(
    title="NBA Dashboard API",
    description="API pour exploiter les données NBA",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware, # Cross-Origin Resource Sharing (CORS) to allow frontend to access api
    allow_origins=["http://localhost:5173"],  # Frontend URL (React)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)
app.include_router(teams.router)

@app.get("/")
def root():
    return {"message": "NBA Dashboard API is running 🏀"}