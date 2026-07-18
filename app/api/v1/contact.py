from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contact import ContactMessage
from app.schemas.contact import ContactMessageCreate, ContactMessageStatusUpdate, ContactMessageOut
from app.utils.rate_limiter import RateLimiter

router = APIRouter(tags=["Contact"])
contact_rate_limit = RateLimiter(max_requests=5, window_seconds=60)


@router.post(
    "/contact",
    response_model=ContactMessageOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(contact_rate_limit)],
)
def submit_contact_message(payload: ContactMessageCreate, db: Session = Depends(get_db)):
    message = ContactMessage(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/admin/contact-messages", response_model=list[ContactMessageOut])
def list_contact_messages(db: Session = Depends(get_db)):
    stmt = select(ContactMessage).order_by(ContactMessage.created_at.desc())
    return db.execute(stmt).scalars().all()


@router.patch("/admin/contact-messages/{message_id}/status", response_model=ContactMessageOut)
def update_contact_status(message_id: int, payload: ContactMessageStatusUpdate, db: Session = Depends(get_db)):
    message = db.get(ContactMessage, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    message.status = payload.status
    db.commit()
    db.refresh(message)
    return message


@router.delete("/admin/contact-messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_message(message_id: int, db: Session = Depends(get_db)):
    message = db.get(ContactMessage, message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    db.delete(message)
    db.commit()