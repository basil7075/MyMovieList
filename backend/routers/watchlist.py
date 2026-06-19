from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..database import get_db
from ..models import WatchlistItem
from ..schemas import WatchlistItemCreate, WatchlistItemUpdate, WatchlistItemOut

router = APIRouter(prefix="/watchlist",tags = ["watchlist"])

@router.get("/",response_model = list[WatchlistItemOut])
def get_watchlist(watched: bool | None = None, db: Session = Depends(get_db)):
    
    q = db.query(WatchlistItem)
    if watched is not None:
        q = q.filter(WatchlistItem.watched == watched)
    
    return q.order_by(WatchlistItem.added_at.desc()).all()

@router.post("/",response_model = WatchlistItemOut, status_code = 201)
def add_to_watchlist(item:WatchlistItemCreate, db:Session = Depends(get_db)):
    
    existing = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.tmdb_id == item.tmdb_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code = 409, detail = "Already in watchlist")

    db_item = WatchlistItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

@router.patch("/{tmdb_id}",response_model = WatchlistItemOut)
def update_item(tmdb_id: int, update: WatchlistItemUpdate, db: Session = Depends(get_db)):
    
    item = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.tmdb_id == tmdb_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code = 404, detail = "Not in watchlist")
    
    if update.watched is not None:
        item.watched = update.watched
        item.watched_at = (datetime.now(timezone.utc)) if update.watched else None

    if update.rating is not None:
        item.rating = update.rating

    db.commit()
    db.refresh(item)

    return item

@router.delete("/{tmdb_id}",status_code = 204)
def remove_from_watchlist(tmdb_id:int, db:Session = Depends(get_db)):

    item = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.tmdb_id == tmdb_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code = 404, detail = "Not in watchlist")
    
    db.delete(item)
    db.commit()