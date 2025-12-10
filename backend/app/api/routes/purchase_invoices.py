from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.purchase import PurchaseInvoice
from app.schemas.purchase import PurchaseInvoiceCreate, PurchaseInvoiceOut
from app.services.purchase_service import PurchaseService

router = APIRouter()


@router.get('/', response_model=list[PurchaseInvoiceOut])
def list_purchase_invoices(
    db: Session = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = 0,
    supplier_id: int | None = None,
):
    query = db.query(PurchaseInvoice)
    if supplier_id:
        query = query.filter(PurchaseInvoice.supplier_id == supplier_id)
    return query.offset(offset).limit(limit).all()


@router.get('/{invoice_id}', response_model=PurchaseInvoiceOut)
def get_purchase_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.get(PurchaseInvoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invoice not found')
    return invoice


@router.post('/', response_model=PurchaseInvoiceOut, dependencies=[Depends(get_current_active_admin)])
def create_purchase_invoice(invoice_in: PurchaseInvoiceCreate, db: Session = Depends(get_db)):
    service = PurchaseService(db)
    invoice = service.create_invoice(invoice_in)
    return invoice
