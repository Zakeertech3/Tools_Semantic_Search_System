from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.postgres import get_db
from app.schemas.tool import ToolCreate, ToolUpdate, ToolResponse
from app.services.tool_service import tool_service

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/", response_model=ToolResponse)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    created_tool = tool_service.create_tool(db, tool)
    return ToolResponse(
        id=created_tool.id,
        name=created_tool.name,
        description=created_tool.description,
        tags=created_tool.tags,
        metadata=created_tool.metadata_,
        vector_id=created_tool.vector_id,
        created_at=created_tool.created_at,
        updated_at=created_tool.updated_at
    )


@router.get("/", response_model=List[ToolResponse])
def get_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tools = tool_service.get_all_tools(db, skip, limit)
    return [
        ToolResponse(
            id=tool.id,
            name=tool.name,
            description=tool.description,
            tags=tool.tags,
            metadata=tool.metadata_,
            vector_id=tool.vector_id,
            created_at=tool.created_at,
            updated_at=tool.updated_at
        )
        for tool in tools
    ]


@router.get("/{tool_id}", response_model=ToolResponse)
def get_tool(tool_id: str, db: Session = Depends(get_db)):
    tool = tool_service.get_tool(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return ToolResponse(
        id=tool.id,
        name=tool.name,
        description=tool.description,
        tags=tool.tags,
        metadata=tool.metadata_,
        vector_id=tool.vector_id,
        created_at=tool.created_at,
        updated_at=tool.updated_at
    )


@router.put("/{tool_id}", response_model=ToolResponse)
def update_tool(tool_id: str, tool: ToolUpdate, db: Session = Depends(get_db)):
    updated_tool = tool_service.update_tool(db, tool_id, tool)
    if not updated_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return ToolResponse(
        id=updated_tool.id,
        name=updated_tool.name,
        description=updated_tool.description,
        tags=updated_tool.tags,
        metadata=updated_tool.metadata_,
        vector_id=updated_tool.vector_id,
        created_at=updated_tool.created_at,
        updated_at=updated_tool.updated_at
    )


@router.delete("/{tool_id}")
def delete_tool(tool_id: str, db: Session = Depends(get_db)):
    success = tool_service.delete_tool(db, tool_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"message": "Tool deleted successfully"}