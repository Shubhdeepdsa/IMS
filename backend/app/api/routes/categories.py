from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.category import PartCategory
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter()


@router.get('/', response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
):
    return db.query(PartCategory).offset(offset).limit(limit).all()


@router.get('/{category_id}', response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(PartCategory, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    return category


@router.post('/', response_model=CategoryOut, dependencies=[Depends(get_current_active_admin)])
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    category = PartCategory(**category_in.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put('/{category_id}', response_model=CategoryOut, dependencies=[Depends(get_current_active_admin)])
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.get(PartCategory, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    for field, value in category_in.dict(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete('/{category_id}', response_model=CategoryOut, dependencies=[Depends(get_current_active_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(PartCategory, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    category.is_active = False
    db.commit()
    db.refresh(category)
    return category
