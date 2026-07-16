"""
Pydantic schemas for Booking Requests — request/response validation.

Schema reference: SRS Section 9.7 (booking_requests table) + Section 10.7 (API)
Owner: Ayesha Nazish
"""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.booking import BookingStatus

# Basic international-friendly phone pattern: optional +, 7-15 digits.
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


class BookingRequestCreate(BaseModel):
    """
    Payload for POST /booking-requests (public, rate-limited).
    This is a lead-generation form, not a scheduling engine —
    preferred_date stays free text (Section 4).
    """

    full_name: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., max_length=50)
    email: EmailStr | None = None
    service_id: int | None = None
    preferred_date: str | None = Field(default=None, max_length=50)
    message: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Reject obviously malformed phone numbers (Section 10.16 — global validation rules)."""
        if not PHONE_REGEX.match(value):
            raise ValueError("Invalid phone number format. Use digits only, optionally prefixed with '+'.")
        return value


class BookingRequestStatusUpdate(BaseModel):
    """Payload for PATCH /admin/booking-requests/{id}/status."""
    status: BookingStatus


class BookingRequestOut(BaseModel):
    """Response schema for admin GET /admin/booking-requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    email: str | None
    service_id: int | None
    preferred_date: str | None
    message: str | None
    status: BookingStatus
    created_at: datetime
    updated_at: datetime