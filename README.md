# MusicWeather Backend

Python backend for **MusicWeather**, a personal music and weather tracking application.

The backend provides the API and manages music listening history, artist statistics, genre rankings, and weather data.

## Technologies

* Python

* FastAPI

* PostgreSQL

* psycopg2

* Requests

* Uvicorn

* uv

## Features

* Listening history API

* Artist statistics and rankings

* Genre statistics and rankings

* Listening activity heatmap

* Weather history API

* Daily weather summaries

* Dashboard data

* PostgreSQL data storage

* Music and weather data synchronization

## Installation

Clone the repository and install the dependencies:

```bash
uv sync
```

## Development

Start the FastAPI server:

```bash
uv run uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Listening

* `GET /listening/history` — Get listening history

* `GET /listening/period` — Get listening activity by period of day

### Artist

* `GET /artist` — Get artist statistics

### Artist Ranking

* `POST /ranking/weekly` — Generate weekly artist ranking

* `POST /ranking/monthly` — Generate monthly artist ranking

### Genres

* `GET /top` — Get top genres

* `GET /period` — Get genre statistics by period of day

### Genres Rankings

* `POST /weekly` — Generate weekly genre ranking

* `POST /monthly` — Generate monthly genre ranking

### Weather

* `GET /weather/history` — Get hourly weather history

* `GET /weather/daily` — Get daily weather summaries

### Dashboard

* `GET /dashboard` — Get dashboard data

### Activity

* `GET /activity/heatmap` — Get listening activity heatmap data

### Health Check

* `GET /` — Check whether the API is running

For detailed parameters, request bodies, responses, and interactive testing, use the FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend

The backend is used by the MusicWeather Vue.js frontend:

https://github.com/i-marasco/MusicWeather-frontend

Make sure the backend is running before starting the frontend.
