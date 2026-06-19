from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class WatchlistItem(Base):
    __tablename__ = "watchlist"
    id = Column(Integer,primary_key=True,index=True)
    tmdb_id = Column(Integer,unique=True,index=True,nullable=False)
    title = Column(String,nullable=False)
    poster_path = Column(String,nullable=True)
    release_year = Column(String,nullable=True)
    genres = Column(String,nullable=True)
    overview = Column(Text,nullable=True)
    watched = Column(Boolean,default=False)
    rating = Column(Float,nullable=True)
    added_at = Column(DateTime(timezone=True),server_default=func.now())
    watched_at = Column(DateTime(timezone=True),nullable=True)