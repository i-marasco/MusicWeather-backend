from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.listening import router as listening_router
from app.api.artist import router as artist_router
from app.api.artist_ranking import router as artist_ranking_router
from app.api.genres import router as genres_router
from app.api.genre_ranking import router as genre_ranking_router
from app.api.weather import router as weather_router

app = FastAPI(title="Spotify Weather API")

# Allow Vue frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listening_router, prefix="/listening", tags=["Listening"])
app.include_router(artist_router, tags=["Artist"])
app.include_router(artist_ranking_router, prefix="/ranking", tags=["Artist Ranking"])
app.include_router(genres_router, tags=["Genres"])
app.include_router(genre_ranking_router, tags=["Genres Rankings"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
@app.get("/")
def health_check():
    return {"status": "ok"}