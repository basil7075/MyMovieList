# MyMovieList

A personal movie tracking web app inspired by MyAnimeList. Browse trending movies, build a watchlist, mark watched, rate films, and get AI-powered recommendations based on your watch history.

## Stack

- **Backend** — FastAPI, SQLAlchemy, SQLite
- **Frontend** — Vanilla HTML, CSS, JavaScript
- **Movie data** — TMDB API
- **AI recommendations** — Groq (LLaMA 3)

## Features

- Browse trending movies
- Search by title
- Movie detail pages with overview, genres, runtime
- Add movies to watchlist
- Mark as watched
- Rate movies out of 10
- AI recommendations based on your watch history

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/mymovielists.git
cd mymovielists
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
TMDB_API_KEY=your_tmdb_key
GROQ_API_KEY=your_groq_key
```

- TMDB — free at https://www.themoviedb.org/settings/api
- Groq — free at https://console.groq.com

### 4. Run

```bash
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## Project Structure

```
mymovielists/
├── backend/
│   ├── main.py              # App entry point
│   ├── config.py            # API keys and settings
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── movies.py        # Browse and search endpoints
│   │   ├── watchlist.py     # Watchlist CRUD endpoints
│   │   └── ai.py            # AI recommendations endpoint
│   └── services/
│       ├── tmdb_service.py  # TMDB API calls
│       └── ai_service.py    # Groq API calls
└── frontend/
    ├── index.html           # Browse and search
    ├── movie.html           # Movie detail
    ├── watchlist.html       # Watchlist
    ├── style.css            # Styles
    └── app.js               # API client and utilities
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /movies/trending | Trending movies |
| GET | /movies/search?q= | Search movies |
| GET | /movies/{id} | Movie detail |
| GET | /watchlist/ | Get watchlist |
| POST | /watchlist/ | Add to watchlist |
| PATCH | /watchlist/{id} | Update watched status or rating |
| DELETE | /watchlist/{id} | Remove from watchlist |
| GET | /ai/recommendations | AI recommendations |
