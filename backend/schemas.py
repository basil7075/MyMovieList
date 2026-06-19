from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WatchlistItemCreate(BaseModel):
    tmdb_id:int
    title:str
    poster_path:Optional[str] = None
    release_year:Optional[str] = None
    genres:Optional[str] = None
    overview:Optional[str] = None

class WatchlistItemUpdate(BaseModel):
    watched:Optional[bool] = None
    rating:Optional[float] = Field(None,ge=1,le=10)

class WatchlistItemOut(BaseModel):
    id:int
    tmdb_id:int
    title:str
    poster_path:Optional[str]
    release_year:Optional[str]
    genres:Optional[str]
    overview:Optional[str]
    watched:bool
    rating:Optional[float]
    added_at:datetime
    watched_at:Optional[datetime]
    model_config = {"from_attributes":True}

class MovieSummary(BaseModel):
    tmdb_id:int
    title:str
    poster_path:Optional[str]
    release_year:Optional[str]
    overview:Optional[str]
    vote_average:Optional[float]

class MovieDetail(MovieSummary):
    genres:Optional[str]
    runtime:Optional[int]
    tagline:Optional[str]
    in_watchlist:bool = False
    watched:bool = False
    rating:Optional[float] = None

class RecommendationOut(BaseModel):
    title:str
    reason:str