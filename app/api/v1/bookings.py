from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import BookingRequest
from app.schemas.booking import BookingRequestCreate, BookingRequestStatusUpdate, BookingRequestOut
from app.utils.rate_limiter import RateLimiter

router = APIRouter(tags=["Booking Requests"])
booking_rate_limit = RateLimiter(max_requests=5, window_seconds=60)


@router.post(
    "/booking-requests",
    response_model=BookingRequestOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(booking_rate_limit)],
)
def create_booking_request(payload: BookingRequestCreate, db: Session = Depends(get_db)):
    booking = BookingRequest(**payload.model_dump())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/admin/booking-requests", response_model=list[BookingRequestOut])
def list_booking_requests(db: Session = Depends(get_db)):
    stmt = select(BookingRequest).order_by(BookingRequest.created_at.desc())
    return db.execute(stmt).scalars().all()


@router.patch("/admin/booking-requests/{booking_id}/status", response_model=BookingRequestOut)
def update_booking_status(booking_id: int, payload: BookingRequestStatusUpdate, db: Session = Depends(get_db)):
    booking = db.get(BookingRequest, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/admin/booking-requests/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_request(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(BookingRequest, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking request not found")
    db.delete(booking)
    db.commit()