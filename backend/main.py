from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NBA Dashboard API",
    description="API pour exploiter les données NBA",
    version="1.0.0"
)

# Autorise le frontend React à communiquer avec le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # port par défaut de Vite (React)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "NBA Dashboard API is running 🏀"}