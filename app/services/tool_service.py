from sqlalchemy.orm import Session
from app.models.tool import Tool
from app.models.search_history import SearchHistory
from app.schemas.tool import ToolCreate, ToolUpdate
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
import time


class ToolService:
    def create_tool(self, db: Session, tool_data: ToolCreate):
        combined_text = f"{tool_data.name} {tool_data.description} {' '.join(tool_data.tags)}"
        embedding = embedding_service.generate_embedding(combined_text)
        
        tool = Tool(
            name=tool_data.name,
            description=tool_data.description,
            tags=tool_data.tags,
            metadata_=tool_data.metadata
        )
        db.add(tool)
        db.commit()
        db.refresh(tool)
        
        payload = {
            "id": str(tool.id),
            "name": tool.name,
            "description": tool.description,
            "tags": tool.tags
        }
        vector_id = qdrant_service.insert_vector(embedding, payload)
        
        tool.vector_id = vector_id
        db.commit()
        db.refresh(tool)
        
        return tool

    def get_tool(self, db: Session, tool_id: str):
        return db.query(Tool).filter(Tool.id == tool_id).first()

    def get_all_tools(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Tool).offset(skip).limit(limit).all()

    def update_tool(self, db: Session, tool_id: str, tool_data: ToolUpdate):
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return None
        
        update_data = tool_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "metadata":
                setattr(tool, "metadata_", value)
            else:
                setattr(tool, field, value)
        
        combined_text = f"{tool.name} {tool.description} {' '.join(tool.tags)}"
        embedding = embedding_service.generate_embedding(combined_text)
        
        payload = {
            "id": str(tool.id),
            "name": tool.name,
            "description": tool.description,
            "tags": tool.tags
        }
        qdrant_service.update_vector(tool.vector_id, embedding, payload)
        
        db.commit()
        db.refresh(tool)
        return tool

    def delete_tool(self, db: Session, tool_id: str):
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            return False
        
        if tool.vector_id:
            qdrant_service.delete_vector(tool.vector_id)
        
        db.delete(tool)
        db.commit()
        return True

    def search_tools(self, db: Session, query: str, limit: int = 5):
        start_time = time.time()
        
        query_embedding = embedding_service.generate_embedding(query)
        search_results = qdrant_service.search_similar(query_embedding, limit)
        
        results = []
        for result in search_results:
            tool_id = result.payload["id"]
            tool = db.query(Tool).filter(Tool.id == tool_id).first()
            if tool:
                results.append({
                    "id": str(tool.id),
                    "name": tool.name,
                    "description": tool.description,
                    "tags": tool.tags,
                    "metadata": tool.metadata_,
                    "score": result.score
                })
        
        response_time = int((time.time() - start_time) * 1000)
        
        search_history = SearchHistory(
            query=query,
            results=results,
            result_count=len(results),
            response_time_ms=response_time
        )
        db.add(search_history)
        db.commit()
        
        return results, response_time


tool_service = ToolService()