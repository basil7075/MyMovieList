# MyMovieList

Browse movies, build a watchlist, mark watched, rate, and get AI-powered recommendations.

**Stack:** FastAPI · SQLite + SQLAlchemy · TMDB API · Groq · Vanilla HTML/CSS/JS

## Setup

```bash
# 1. Clone and install
cd mymovielists
pip install -r requirements.txt

# 2. Add your API keys
cp .env.example .env
# Edit .env — add TMDB_API_KEY and GROQ_API_KEY

# 3. Run
uvicorn backend.main:app --reload
```

Open http://localhost:8000 in your browser.

## API keys

- **TMDB** — free at https://www.themoviedb.org/settings/api
- **Groq** — free at https://console.groq.com

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /movies/trending | Trending movies |
| GET | /movies/search?q= | Search TMDB |
| GET | /movies/{id} | Movie detail + watchlist state |
| GET | /watchlist/ | Your watchlist |
| POST | /watchlist/ | Add movie |
| PATCH | /watchlist/{id} | Mark watched / rate |
| DELETE | /watchlist/{id} | Remove |
| GET | /ai/recommendations | Groq-powered recommendations |
