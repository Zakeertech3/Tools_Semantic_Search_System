from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from app.database.qdrant import get_qdrant_client
from app.config.settings import settings
from uuid import uuid4


class QdrantService:
    def __init__(self):
        self.client = get_qdrant_client()
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def insert_vector(self, vector: list, payload: dict):
        point_id = str(uuid4())
        point = PointStruct(id=point_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return point_id

    def search_similar(self, query_vector: list, limit: int = 5):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return search_result

    def update_vector(self, point_id: str, vector: list, payload: dict):
        point = PointStruct(id=point_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def delete_vector(self, point_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[point_id]
        )


qdrant_service = QdrantService()