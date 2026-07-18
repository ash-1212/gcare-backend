import json
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.settings import WebsiteSetting
from app.schemas.settings import WebsiteSettingsUpdate, WebsiteSettingsOut

router = APIRouter(tags=["Settings"])


def _row_to_dict(rows: list[WebsiteSetting]) -> dict:
    """Convert key-value rows into a flat dict; whatsapp_numbers parsed from JSON."""
    data = {}
    for row in rows:
        if row.setting_key == "whatsapp_numbers":
            try:
                data[row.setting_key] = json.loads(row.setting_value) if row.setting_value else []
            except json.JSONDecodeError:
                data[row.setting_key] = []
        else:
            data[row.setting_key] = row.setting_value
    return data


@router.get("/settings", response_model=WebsiteSettingsOut)
def get_public_settings(db: Session = Depends(get_db)):
    rows = db.execute(select(WebsiteSetting)).scalars().all()
    return WebsiteSettingsOut(**_row_to_dict(rows))


@router.get("/admin/settings", response_model=WebsiteSettingsOut)
def get_admin_settings(db: Session = Depends(get_db)):
    rows = db.execute(select(WebsiteSetting)).scalars().all()
    return WebsiteSettingsOut(**_row_to_dict(rows))


@router.put("/admin/settings", response_model=WebsiteSettingsOut)
def update_settings(payload: WebsiteSettingsUpdate, db: Session = Depends(get_db)):
    """Upsert each key-value pair. whatsapp_numbers stored as JSON string."""
    update_data = payload.model_dump()

    for key, value in update_data.items():
        stored_value = json.dumps(value) if key == "whatsapp_numbers" else value

        row = db.execute(
            select(WebsiteSetting).where(WebsiteSetting.setting_key == key)
        ).scalar_one_or_none()

        if row:
            row.setting_value = stored_value
        else:
            db.add(WebsiteSetting(setting_key=key, setting_value=stored_value))

    db.commit()
    rows = db.execute(select(WebsiteSetting)).scalars().all()
    return WebsiteSettingsOut(**_row_to_dict(rows))