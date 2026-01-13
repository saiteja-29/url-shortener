from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class URLAnalytics(Base):
    __tablename__ = "url_analytics"

    id = Column(BigInteger, primary_key=True)
    url_id = Column(BigInteger, ForeignKey("urls.id"), index=True)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    referrer = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
