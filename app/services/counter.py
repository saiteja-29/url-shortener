from sqlalchemy.orm import Session
from app.models.url import URL


def increment_click_count(db: Session, url_id: int):
    db.query(URL).filter(URL.id == url_id).update(
        {URL.click_count: URL.click_count + 1}
    )
    db.commit()
