from sqlalchemy import Column, String, Text, Integer, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database.postgres import Base
import uuid


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(Text, nullable=False)
    results = Column(JSONB, default=[])
    result_count = Column(Integer, default=0)
    search_timestamp = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    response_time_ms = Column(Integer, default=0)