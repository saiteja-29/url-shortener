from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.services.shortener import URLShortenerService
from app.core.config import settings
router = APIRouter()


@router.post("/shorten")
def shorten_url(payload: dict, db: Session = Depends(get_db)):
    original_url = payload.get("original_url")
    expires_in_days = payload.get("expires_in_days")

    if not original_url:
        raise HTTPException(status_code=400, detail="original_url is required")

    expires_at = None
    if expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

    url = URLShortenerService.create_or_get_short_url(
        db=db,
        original_url=original_url,
        expires_at=expires_at
    )

    return {
        "short_code": url.short_code,
        "short_url": f"{settings.BASE_URL}/{url.short_code}"
    }
