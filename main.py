from fastapi import FastAPI
from app.api.listening import router as listening_router
from app.api.artist import router as artist_router
from app.clients.artist_ranking import router as artist_ranking_router

app = FastAPI(title="Spotify Weather API")

app.include_router(listening_router, prefix="/listening", tags=["Listening"])
app.include_router(artist_router, tags=["Artist"])
app.include_router(artist_ranking_router, prefix="/ranking", tags=["Artist Ranking"])

@app.get("/")
def health_check():
    return {"status": "ok"}