from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.sales import SalesInvoice
from app.schemas.sales import SalesInvoiceCreate, SalesInvoiceOut
from app.services.sales_service import SalesService

router = APIRouter()


@router.get('/', response_model=list[SalesInvoiceOut])
def list_sales_invoices(
    db: Session = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = 0,
    customer_id: int | None = None,
):
    query = db.query(SalesInvoice)
    if customer_id:
        query = query.filter(SalesInvoice.customer_id == customer_id)
    return query.offset(offset).limit(limit).all()


@router.get('/{invoice_id}', response_model=SalesInvoiceOut)
def get_sales_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.get(SalesInvoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invoice not found')
    return invoice


@router.post('/', response_model=SalesInvoiceOut, dependencies=[Depends(get_current_active_admin)])
def create_sales_invoice(invoice_in: SalesInvoiceCreate, db: Session = Depends(get_db)):
    service = SalesService(db)
    invoice = service.create_invoice(invoice_in)
    return invoice
