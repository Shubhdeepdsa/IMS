from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.part import Part
from app.schemas.part import PartOut

router = APIRouter()


@router.get('/stock', response_model=list[PartOut])
def stock_report(db: Session = Depends(get_db), limit: int = Query(100, le=500), offset: int = 0, is_active: bool | None = None):
    query = db.query(Part)
    if is_active is not None:
        query = query.filter(Part.is_active == is_active)
    return query.order_by(Part.name).offset(offset).limit(limit).all()


@router.get('/low-stock', response_model=list[PartOut])
def low_stock_report(db: Session = Depends(get_db), limit: int = Query(100, le=500), offset: int = 0):
    query = db.query(Part).filter(Part.current_stock <= Part.min_stock_level)
    return query.order_by(Part.name).offset(offset).limit(limit).all()
