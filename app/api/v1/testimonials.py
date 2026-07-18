from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialOut

router = APIRouter(tags=["Testimonials"])


@router.get("/testimonials", response_model=list[TestimonialOut])
def list_testimonials(db: Session = Depends(get_db)):
    stmt = (
        select(Testimonial)
        .where(Testimonial.is_active == True)  # noqa: E712
        .order_by(Testimonial.display_order.asc(), Testimonial.created_at.desc())
    )
    return db.execute(stmt).scalars().all()


@router.post("/admin/testimonials", response_model=TestimonialOut, status_code=status.HTTP_201_CREATED)
def create_testimonial(payload: TestimonialCreate, db: Session = Depends(get_db)):
    testimonial = Testimonial(**payload.model_dump())
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.put("/admin/testimonials/{testimonial_id}", response_model=TestimonialOut)
def update_testimonial(testimonial_id: int, payload: TestimonialUpdate, db: Session = Depends(get_db)):
    testimonial = db.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(testimonial, field, value)
    db.commit()
    db.refresh(testimonial)
    return testimonial


@router.delete("/admin/testimonials/{testimonial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    testimonial = db.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    db.delete(testimonial)
    db.commit()