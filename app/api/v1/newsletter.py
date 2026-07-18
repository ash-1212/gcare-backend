from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.newsletter import NewsletterSubscriber
from app.schemas.newsletter import (
    NewsletterSubscribeRequest,
    NewsletterUnsubscribeRequest,
    NewsletterSubscriberOut,
)
from app.utils.rate_limiter import RateLimiter

router = APIRouter(tags=["Newsletter"])
newsletter_rate_limit = RateLimiter(max_requests=5, window_seconds=60)


@router.post(
    "/newsletter/subscribe",
    response_model=NewsletterSubscriberOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(newsletter_rate_limit)],
)
def subscribe(payload: NewsletterSubscribeRequest, db: Session = Depends(get_db)):
    existing = db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == payload.email)
    ).scalar_one_or_none()

    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            db.refresh(existing)
        return existing

    subscriber = NewsletterSubscriber(email=payload.email)
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber


@router.post("/newsletter/unsubscribe", status_code=status.HTTP_200_OK)
def unsubscribe(payload: NewsletterUnsubscribeRequest, db: Session = Depends(get_db)):
    subscriber = db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == payload.email)
    ).scalar_one_or_none()
    if not subscriber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscriber not found")
    subscriber.is_active = False
    db.commit()
    return {"message": "Unsubscribed successfully"}


@router.get("/admin/newsletter", response_model=list[NewsletterSubscriberOut])
def list_subscribers(db: Session = Depends(get_db)):
    stmt = select(NewsletterSubscriber).order_by(NewsletterSubscriber.created_at.desc())
    return db.execute(stmt).scalars().all()


@router.delete("/admin/newsletter/{subscriber_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    subscriber = db.get(NewsletterSubscriber, subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscriber not found")
    db.delete(subscriber)
    db.commit()