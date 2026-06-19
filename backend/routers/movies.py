from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import WatchlistItem
from ..services import tmdb_service
from ..schemas import RecommendationOut

router = APIRouter(prefix = "/movies",tags = ["movies"])

@router.get("/trending")
async def trending():

    try:
        return await tmdb_service.get_trending()
    except Exception as e:
        raise HTTPException(status_code=502,detail=f"TMDB error: {e}")

@router.get("/search")
async def search(q: str = Query(...,min_length=1),page: int = 1):

    try:
        return await tmdb_service.search_movies(q,page)
    except Exception as e:
        raise HTTPException(status_code=502,detail=f"TMDB error: {e}")

@router.get("/{tmdb_id}")
async def movie_detail(tmdb_id:int,db: Session = Depends(get_db)):

    try:
        detail = await tmdb_service.get_movie_detail(tmdb_id)
    except Exception as e:
        raise HTTPException(status_code=502,detail=f"TMDB error: {e}")

    item = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.tmdb_id == tmdb_id)
        .first()
    )

    detail["in_watchlist"] = item is not None
    detail["watched"] = item.watched if item else False
    detail["rating"] = item.rating if item else None

    return detail