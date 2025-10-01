from sentence_transformers import SentenceTransformer
from app.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: list):
        embeddings = self.model.encode(texts)
        return [embedding.tolist() for embedding in embeddings]


embedding_service = EmbeddingService()