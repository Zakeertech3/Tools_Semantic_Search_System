from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal
from app.models.tool import Tool
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service

def sync_tools_to_qdrant():
    db = SessionLocal()
    try:
        tools = db.query(Tool).filter(Tool.vector_id == None).all()
        
        print(f"Found {len(tools)} tools without vector embeddings")
        
        for tool in tools:
            combined_text = f"{tool.name} {tool.description} {' '.join(tool.tags)}"
            embedding = embedding_service.generate_embedding(combined_text)
            
            payload = {
                "id": str(tool.id),
                "name": tool.name,
                "description": tool.description,
                "tags": tool.tags
            }
            
            vector_id = qdrant_service.insert_vector(embedding, payload)
            tool.vector_id = vector_id
            db.commit()
            
            print(f"Synced: {tool.name}")
        
        print("Sync complete!")
        
    finally:
        db.close()

if __name__ == "__main__":
    sync_tools_to_qdrant()