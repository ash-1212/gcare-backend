from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FAQBase(BaseModel):
    question: str = Field(..., min_length=1, max_length=255)
    answer: str = Field(..., min_length=1)
    display_order: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: str | None = Field(default=None, max_length=255)
    answer: str | None = None
    display_order: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class FAQOut(FAQBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime