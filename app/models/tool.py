from sqlalchemy import Column, String, Text, TIMESTAMP, ARRAY, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database.postgres import Base
import uuid


class Tool(Base):
    __tablename__ = "tools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(ARRAY(Text), default=[])
    metadata_ = Column("metadata", JSONB, default={})
    vector_id = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))