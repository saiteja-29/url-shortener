from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(16), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(BigInteger, default=0)
