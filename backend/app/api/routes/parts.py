from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.part import Part
from app.models.supplier import PartSupplier
from app.models.tractor_model import PartCompatibleModel, TractorModel
from app.schemas.part import (
    PartCompatibilityCreate,
    PartCompatibilityOut,
    PartCreate,
    PartOut,
    PartSupplierOut,
    PartSupplierPayload,
    PartUpdate,
)

router = APIRouter()


@router.get('/', response_model=list[PartOut])
def list_parts(
    db: Session = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    category_id: int | None = None,
    supplier_id: int | None = None,
    q: str | None = None,
    tractor_model_id: int | None = None,
):
    query = db.query(Part)
    if category_id:
        query = query.filter(Part.category_id == category_id)
    if supplier_id:
        query = query.join(Part.suppliers).filter(PartSupplier.supplier_id == supplier_id)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Part.name.ilike(like), Part.part_code.ilike(like)))
    if tractor_model_id:
        query = query.join(Part.compatible_models).filter(PartCompatibleModel.tractor_model_id == tractor_model_id)
    return query.offset(offset).limit(limit).all()


@router.get('/{part_id}', response_model=PartOut)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    return part


@router.get('/by-barcode/{barcode_value}', response_model=PartOut)
def get_part_by_barcode(barcode_value: str, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.barcode_value == barcode_value).first()
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    return part


@router.post('/', response_model=PartOut, dependencies=[Depends(get_current_active_admin)])
def create_part(part_in: PartCreate, db: Session = Depends(get_db)):
    part = Part(**part_in.dict(exclude={'suppliers'}))
    db.add(part)
    db.flush()
    if part_in.suppliers:
        for supplier_link in part_in.suppliers:
            link = PartSupplier(part_id=part.id, **supplier_link.dict())
            db.add(link)
    db.commit()
    db.refresh(part)
    return part


@router.put('/{part_id}', response_model=PartOut, dependencies=[Depends(get_current_active_admin)])
def update_part(part_id: int, part_in: PartUpdate, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    for field, value in part_in.dict(exclude_unset=True).items():
        setattr(part, field, value)
    db.commit()
    db.refresh(part)
    return part


@router.delete('/{part_id}', response_model=PartOut, dependencies=[Depends(get_current_active_admin)])
def delete_part(part_id: int, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    part.is_active = False
    db.commit()
    db.refresh(part)
    return part


@router.get('/{part_id}/suppliers', response_model=list[PartSupplierOut])
def get_part_suppliers(part_id: int, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    return part.suppliers


@router.post('/{part_id}/suppliers/{supplier_id}', response_model=PartSupplierOut, dependencies=[Depends(get_current_active_admin)])
def upsert_part_supplier(part_id: int, supplier_id: int, payload: PartSupplierPayload, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    link = (
        db.query(PartSupplier)
        .filter(and_(PartSupplier.part_id == part_id, PartSupplier.supplier_id == supplier_id))
        .first()
    )
    if not link:
        link = PartSupplier(part_id=part_id, supplier_id=supplier_id)
        db.add(link)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(link, field, value)
    db.commit()
    db.refresh(link)
    return link


@router.delete('/{part_id}/suppliers/{supplier_id}', dependencies=[Depends(get_current_active_admin)])
def delete_part_supplier(part_id: int, supplier_id: int, db: Session = Depends(get_db)):
    deleted = (
        db.query(PartSupplier)
        .filter(and_(PartSupplier.part_id == part_id, PartSupplier.supplier_id == supplier_id))
        .delete()
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mapping not found')
    db.commit()
    return {'status': 'deleted'}


@router.get('/{part_id}/compatible-models', response_model=list[PartCompatibilityOut])
def list_compatible_models(part_id: int, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    return part.compatible_models


@router.post('/{part_id}/compatible-models', response_model=PartCompatibilityOut, dependencies=[Depends(get_current_active_admin)])
def add_compatible_model(part_id: int, payload: PartCompatibilityCreate, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    tractor_model = db.get(TractorModel, payload.tractor_model_id)
    if not tractor_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tractor model not found')
    link = PartCompatibleModel(part_id=part_id, tractor_model_id=payload.tractor_model_id)
    db.add(link)
    try:
        db.commit()
    except Exception as exc:  # pragma: no cover
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Compatibility already exists') from exc
    db.refresh(link)
    return link


@router.delete('/{part_id}/compatible-models/{tractor_model_id}', dependencies=[Depends(get_current_active_admin)])
def delete_compatible_model(part_id: int, tractor_model_id: int, db: Session = Depends(get_db)):
    deleted = (
        db.query(PartCompatibleModel)
        .filter(
            PartCompatibleModel.part_id == part_id,
            PartCompatibleModel.tractor_model_id == tractor_model_id,
        )
        .delete()
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Compatibility not found')
    db.commit()
    return {'status': 'deleted'}
