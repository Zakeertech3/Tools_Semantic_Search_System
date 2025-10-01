from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config.settings import settings


def get_qdrant_client():
    client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
    return client


def initialize_collection():
    client = get_qdrant_client()
    
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if settings.QDRANT_COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=settings.VECTOR_SIZE, distance=Distance.COSINE)
        )