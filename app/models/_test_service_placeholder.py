"""
TEMPORARY placeholder — only for standalone local testing of booking_requests FK.
DELETE this file once merged with Rehman's real app/models/service.py.
"""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150))