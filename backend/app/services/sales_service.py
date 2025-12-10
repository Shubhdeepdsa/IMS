from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.part import Part
from app.models.sales import SalesInvoice, SalesInvoiceItem
from app.models.stock_movement import StockMovementType
from app.schemas.sales import SalesInvoiceCreate
from app.services.stock_service import StockService


class SalesService:
    def __init__(self, db: Session):
        self.db = db
        self.stock_service = StockService(db)

    def create_invoice(self, data: SalesInvoiceCreate) -> SalesInvoice:
        if data.customer_id:
            customer = self.db.get(Customer, data.customer_id)
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')

        invoice = SalesInvoice(
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            customer_id=data.customer_id,
            subtotal=data.subtotal,
            total_tax=data.total_tax,
            total_amount=data.total_amount,
            payment_mode=data.payment_mode,
            payment_status=data.payment_status,
            notes=data.notes,
        )

        with self.db.begin():
            self.db.add(invoice)
            self.db.flush()
            for item_data in data.items:
                part = self.db.get(Part, item_data.part_id)
                if not part:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
                self.stock_service.adjust_stock(part, -item_data.quantity, StockMovementType.SALE, invoice.id)
                item = SalesInvoiceItem(
                    invoice=invoice,
                    part_id=item_data.part_id,
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price,
                    discount_amount=item_data.discount_amount,
                    tax_rate_percent=item_data.tax_rate_percent,
                    tax_amount=item_data.tax_amount,
                    line_total=item_data.line_total,
                )
                self.db.add(item)
            self.db.flush()
        self.db.refresh(invoice)
        return invoice
