from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import players, teams

app = FastAPI(
    title="NBA Dashboard API",
    description="API pour exploiter les données NBA",
    version="1.0.0"
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