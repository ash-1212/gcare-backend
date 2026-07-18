from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate, BranchOut

router = APIRouter(tags=["Branches"])


@router.get("/branches", response_model=list[BranchOut])
def list_branches(db: Session = Depends(get_db)):
    """Public: active branches, sorted per Global Sorting Rule."""
    stmt = (
        select(Branch)
        .where(Branch.is_active == True)  # noqa: E712
        .order_by(Branch.display_order.asc(), Branch.created_at.desc())
    )
    return db.execute(stmt).scalars().all()


@router.get("/admin/branches", response_model=list[BranchOut])
def admin_list_branches(db: Session = Depends(get_db)):
    """Admin: all branches including inactive."""
    stmt = select(Branch).order_by(Branch.display_order.asc(), Branch.created_at.desc())
    return db.execute(stmt).scalars().all()


@router.get("/admin/branches/{branch_id}", response_model=BranchOut)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch


@router.post("/admin/branches", response_model=BranchOut, status_code=status.HTTP_201_CREATED)
def create_branch(payload: BranchCreate, db: Session = Depends(get_db)):
    branch = Branch(**payload.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


@router.put("/admin/branches/{branch_id}", response_model=BranchOut)
def update_branch(branch_id: int, payload: BranchUpdate, db: Session = Depends(get_db)):
    branch = db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(branch, field, value)
    db.commit()
    db.refresh(branch)
    return branch


@router.delete("/admin/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    db.delete(branch)
    db.commit()