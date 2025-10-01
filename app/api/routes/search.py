from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.tool_service import tool_service

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
def search_tools(search_request: SearchRequest, db: Session = Depends(get_db)):
    results, response_time = tool_service.search_tools(
        db, 
        search_request.query, 
        search_request.limit
    )
    
    return SearchResponse(
        query=search_request.query,
        results=results,
        result_count=len(results),
        response_time_ms=response_time
    )