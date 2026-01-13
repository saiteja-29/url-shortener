from datetime import datetime
from sqlalchemy.orm import Session
from app.models.url import URL
from app.utils.base62 import encode_base62


class URLShortenerService:

    @staticmethod
    def create_or_get_short_url(
        db: Session,
        original_url: str,
        expires_at: datetime | None = None
    ) -> URL:
        now = datetime.utcnow()

        # Step 1: Check for existing active URL
        existing = (
            db.query(URL)
            .filter(
                URL.original_url == original_url,
                (URL.expires_at.is_(None) | (URL.expires_at > now))
            )
            .first()
        )

        if existing:
            # Step 2: Update expiration if extended
            if expires_at and (
                existing.expires_at is None or expires_at > existing.expires_at
            ):
                existing.expires_at = expires_at
                db.commit()
                db.refresh(existing)

            return existing

        # Step 3: Create new short URL
        url = URL(
            original_url=original_url,
            expires_at=expires_at
        )
        db.add(url)
        db.flush()  # get ID

        url.short_code = encode_base62(url.id)

        db.commit()
        db.refresh(url)

        return url
