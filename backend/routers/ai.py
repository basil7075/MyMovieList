from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import WatchlistItem
from ..services import ai_service
from ..schemas import RecommendationOut

router = APIRouter(prefix="/ai",tags=["ai"])

@router.get("/recommendations",response_model=list[RecommendationOut])
def recommendations(db:Session = Depends(get_db)):
    watched = (db.query(WatchlistItem)
    .filter(WatchlistItem.watched==True)
    .order_by(WatchlistItem.watched_at.desc())
    .all()
    )

    if not watched:
        raise HTTPException(status_code = 400,detail = "No watched movies yet..")

    movies = [{"title":m.title,"genre":m.genres,"rating":m.rating}for m in watched]

    try:
        return ai_service.get_recommendations(movies)

    except Exception as e:
        raise HTTPException(status_code = 502,detail = f"AI error: {e}")