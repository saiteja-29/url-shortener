from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone

from app.db.session import get_db
from app.models.url import URL
from app.services.background import process_analytics

router = APIRouter()


@router.get("/{short_code}")
def redirect(
    short_code: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Not Found")

    if url.expires_at and url.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="URL expired")

    # 🔥 THIS IS WHAT YOU WERE MISSING
    background_tasks.add_task(
        process_analytics,
        url.id,
        request.client.host,
        request.headers.get("user-agent"),
        request.headers.get("referer"),
    )

    return RedirectResponse(url.original_url)
