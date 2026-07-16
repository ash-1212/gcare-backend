"""
Pydantic schemas for Branch — request/response validation.

Schema reference: SRS Section 9.4 (branches table) + Section 10.4 (API)
Owner: Ayesha Nazish
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BranchBase(BaseModel):
    """Shared fields used by both create and update payloads."""

    name: str = Field(..., min_length=1, max_length=150)
    address: str = Field(..., min_length=1)
    phone: str | None = Field(default=None, max_length=50)

    # Matches Numeric(9,6) in the model — 6 decimal places of precision
    # is enough for Google Maps accuracy at street level.
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)

    display_order: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)


class BranchCreate(BranchBase):
    """Payload for POST /admin/branches — all fields required as defined above."""
    pass


class BranchUpdate(BaseModel):
    """
    Payload for PUT /admin/branches/{id}.
    All fields optional — supports partial updates.
    """

    name: str | None = Field(default=None, min_length=1, max_length=150)
    address: str | None = Field(default=None, min_length=1)
    phone: str | None = Field(default=None, max_length=50)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class BranchOut(BranchBase):
    """
    Response schema — used for both public GET /branches
    and admin GET /admin/branches endpoints.
    """

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2: allows reading from ORM objects

    id: int
    created_at: datetime
    updated_at: datetime


class BranchServiceAssign(BaseModel):
    """
    Payload for PUT /admin/branches/{id}/services
    Section 10.4 — sets the linked services for a branch (M:N).
    """
    service_ids: list[int] = Field(default_factory=list)