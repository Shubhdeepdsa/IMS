from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierOut, SupplierUpdate

router = APIRouter()


@router.get('/', response_model=list[SupplierOut])
def list_suppliers(db: Session = Depends(get_db), limit: int = Query(50, le=100), offset: int = 0, is_active: bool | None = None):
    query = db.query(Supplier)
    if is_active is not None:
        query = query.filter(Supplier.is_active == is_active)
    return query.offset(offset).limit(limit).all()


@router.get('/{supplier_id}', response_model=SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')
    return supplier


@router.post('/', response_model=SupplierOut, dependencies=[Depends(get_current_active_admin)])
def create_supplier(supplier_in: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**supplier_in.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.put('/{supplier_id}', response_model=SupplierOut, dependencies=[Depends(get_current_active_admin)])
def update_supplier(supplier_id: int, supplier_in: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')
    for field, value in supplier_in.dict(exclude_unset=True).items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.delete('/{supplier_id}', response_model=SupplierOut, dependencies=[Depends(get_current_active_admin)])
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.get(Supplier, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')
    supplier.is_active = False
    db.commit()
    db.refresh(supplier)
    return supplier
