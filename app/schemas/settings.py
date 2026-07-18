from pydantic import BaseModel, Field


class WebsiteSettingsUpdate(BaseModel):
    """Bulk update payload — matches SRS Section 10.15(B), WhatsApp as array."""
    whatsapp_numbers: list[str] = Field(default_factory=list)
    phone_1: str | None = None
    phone_2: str | None = None
    email: str | None = None
    facebook_url: str | None = None
    instagram_url: str | None = None
    hero_title: str | None = None
    hero_subtitle: str | None = None


class WebsiteSettingsOut(BaseModel):
    """Response — flattened key-value dict resolved from the DB rows."""
    whatsapp_numbers: list[str] = Field(default_factory=list)
    phone_1: str | None = None
    phone_2: str | None = None
    email: str | None = None
    facebook_url: str | None = None
    instagram_url: str | None = None
    hero_title: str | None = None
    hero_subtitle: str | None = None