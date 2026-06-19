import aiohttp
from ..config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE

def _poster_url(path:str|None) -> str|None:

    return f"{TMDB_IMAGE_BASE}{path}" if path else None

def _year(date_str:str|None) -> str|None:

    return date_str[:4] if date_str else None

async def search_movies(query:str, page:int = 1) -> dict:

    url = f"{TMDB_BASE_URL}/search/movie"

    params = {"api_key" : TMDB_API_KEY, "query" : query, "page" : page }

    async with aiohttp.ClientSession() as session:
        async with session.get(url,params = params) as resp:
            resp.raise_for_status()
            data = await resp.json()

    results = [
        {
            "tmdb_id":m["id"],
            "title":m["title"],
            "poster_path":_poster_url(m.get("poster_path")),
            "release_year":_year(m.get("release_date")),
            "overview":m.get("overview"),
            "vote_average":m.get("vote_average"),
        }
        for m in data.get("results",[])
    ]

    return {
        "results":results,
        "total_pages":data.get("total_pages",1),
        "page":page
    }

async def get_movie_detail(tmdb_id:int) -> dict:
    
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"

    params = {"api_key":TMDB_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params = params) as resp:
            resp.raise_for_status()
            m = await resp.json()
    
    return {
        "tmdb_id": m["id"],
        "title": m["title"],
        "poster_path": _poster_url(m.get("poster_path")),
        "release_year": _year(m.get("release_date")),
        "overview": m.get("overview"),
        "vote_average": m.get("vote_average"),
        "genres":", ".join(g["name"] for g in m.get("genres",[])),
        "runtime":m.get("runtime"),
        "tagline":m.get("tagline"),
    }

async def get_trending(time_window: str = "week") -> list:

    url = f"{TMDB_BASE_URL}/trending/movie/{time_window}"

    params = {"api_key":TMDB_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(url,params = params) as resp:
            resp.raise_for_status()
            data = await resp.json()

    return [
        {
            "tmdb_id": m["id"],
            "title": m["title"],
            "poster_path": _poster_url(m.get("poster_path")),
            "release_year": _year(m.get("release_date")),
            "overview": m.get("overview"),
            "vote_average": m.get("vote_average"),
        }
        for m in data.get("results", [])[:18]
    ]