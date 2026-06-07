from fastapi import FastAPI
from app.api.listening import router as listening_router
from app.api.artist import router as artist_router
from app.clients.artist_ranking import router as artist_ranking_router


# http://localhost:8000/artist?start_date=2026-05-30 00:00:00&end_date=2026-05-30 00:00:00
# http://127.0.0.1:8000/listening?start_date=2026-05-29%2000:00:00&end_date=2026-05-29%2023:59:59
# http://127.0.0.1:8000/listening/artist?start_date=2026-05-29%2000:00:00&end_date=2026-05-29%2023:59:59
# http://127.0.0.1:8000/listening/history?start_date=2026-05-29%2000:00:00&end_date=2026-05-29%2023:59:59

app = FastAPI(title="Spotify Weather API")

app.include_router(listening_router, prefix="/listening", tags=["Listening"])
app.include_router(artist_router, tags=["Artist"])
app.include_router(artist_ranking_router, prefix="/ranking", tags=["Artist Ranking"])

@app.get("/")
def health_check():
    return {"status": "ok"}