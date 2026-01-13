from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone

from app.db.session import get_db
from app.models.url import URL
from app.models.analytics import URLAnalytics

router = APIRouter()


@router.get("/stats/{short_code}")
def get_stats(short_code: str, db: Session = Depends(get_db)):
    # 1️⃣ Find URL
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # 2️⃣ Last 24 hours count
    last_24_hours = (
        db.query(URLAnalytics)
        .filter(
            URLAnalytics.url_id == url.id,
            URLAnalytics.created_at >= datetime.now(timezone.utc) - timedelta(hours=24)
        )
        .count()
    )

    # 3️⃣ Recent clicks (limit)
    recent_clicks = (
        db.query(URLAnalytics)
        .filter(URLAnalytics.url_id == url.id)
        .order_by(URLAnalytics.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "short_code": url.short_code,
        "original_url": url.original_url,
        "total_clicks": url.click_count,
        "last_24_hours": last_24_hours,
        "recent_clicks": [
            {
                "ip": a.ip_address,
                "user_agent": a.user_agent,
                "time": a.created_at.isoformat() if a.created_at else None
            }
            for a in recent_clicks
        ]
    }


