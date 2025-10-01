from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    id: UUID
    name: str
    description: str
    tags: List[str]
    metadata: dict
    score: float

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    result_count: int
    response_time_ms: int