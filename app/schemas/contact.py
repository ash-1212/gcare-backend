import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.contact import ContactStatus

PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


class ContactMessageCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., max_length=50)
    message: str = Field(..., min_length=1)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_REGEX.match(value):
            raise ValueError("Invalid phone number format.")
        return value


class ContactMessageStatusUpdate(BaseModel):
    status: ContactStatus


class ContactMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    phone: str
    message: str
    status: ContactStatus
    created_at: datetime
    updated_at: datetime