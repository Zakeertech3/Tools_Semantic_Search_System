from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID


class ToolBase(BaseModel):
    name: str
    description: str
    tags: List[str] = []
    metadata: Dict = {}


class ToolCreate(ToolBase):
    pass


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict] = None


class ToolResponse(ToolBase):
    id: UUID
    vector_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def model_validate(cls, obj):
        if hasattr(obj, 'metadata_'):
            obj.metadata = obj.metadata_
        return super().model_validate(obj)