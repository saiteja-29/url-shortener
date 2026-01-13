from sqlalchemy.orm import Session
from app.models.analytics import URLAnalytics


def log_click(
    db: Session,
    url_id: int,
    ip_address: str,
    user_agent: str,
    referrer: str | None = None
):
    analytics = URLAnalytics(
        url_id=url_id,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer
    )

    db.add(analytics)
    db.commit()
