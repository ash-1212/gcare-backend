"""
Booking Request model — patient service booking / lead-generation requests.

Schema reference: SRS Section 9.7 (booking_requests table)
Owner: Ayesha Nazish
"""

import enum
from datetime import datetime

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class BookingStatus(str, enum.Enum):
    """Status lifecycle for a booking request (Section 9.7)."""
    pending = "pending"
    contacted = "contacted"
    completed = "completed"


class BookingRequest(Base):
    """
    Represents a lead-generation booking submitted from the public
    "Book Now" modal on Services / Service Detail pages.
    """

    __tablename__ = "booking_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)

    service_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("services.id", ondelete="SET NULL"),
        nullable=True,
    )

    preferred_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status"),
        default=BookingStatus.pending,
        server_default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<BookingRequest id={self.id} name={self.full_name!r} status={self.status}>"