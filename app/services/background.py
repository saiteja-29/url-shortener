from app.db.session import SessionLocal
from app.services.analytics import log_click
from app.services.counter import increment_click_count


def process_analytics(
    url_id: int,
    ip: str,
    user_agent: str | None,
    referrer: str | None
):
    db = SessionLocal()
    try:
        increment_click_count(db, url_id)
        log_click(db, url_id, ip, user_agent, referrer)
    finally:
        db.close()
