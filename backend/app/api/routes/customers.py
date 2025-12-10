from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate

router = APIRouter()


@router.get('/', response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db), limit: int = Query(50, le=100), offset: int = 0):
    return db.query(Customer).offset(offset).limit(limit).all()


@router.get('/{customer_id}', response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    return customer


@router.post('/', response_model=CustomerOut, dependencies=[Depends(get_current_active_admin)])
def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db)):
    customer = Customer(**customer_in.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.put('/{customer_id}', response_model=CustomerOut, dependencies=[Depends(get_current_active_admin)])
def update_customer(customer_id: int, customer_in: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    for field, value in customer_in.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


@router.delete('/{customer_id}', response_model=CustomerOut, dependencies=[Depends(get_current_active_admin)])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    customer.is_active = False
    db.commit()
    db.refresh(customer)
    return customer
