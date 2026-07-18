from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TestimonialBase(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=150)
    feedback: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    patient_name: str | None = Field(default=None, max_length=150)
    feedback: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class TestimonialOut(TestimonialBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime