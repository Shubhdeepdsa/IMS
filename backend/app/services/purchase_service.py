from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.part import Part
from app.models.purchase import PurchaseInvoice, PurchaseInvoiceItem
from app.models.stock_movement import StockMovementType
from app.models.supplier import PartSupplier, Supplier
from app.schemas.purchase import PurchaseInvoiceCreate
from app.services.stock_service import StockService


class PurchaseService:
    def __init__(self, db: Session):
        self.db = db
        self.stock_service = StockService(db)

    def create_invoice(self, data: PurchaseInvoiceCreate) -> PurchaseInvoice:
        supplier = self.db.get(Supplier, data.supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

        invoice = PurchaseInvoice(
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            supplier_id=data.supplier_id,
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
                item = PurchaseInvoiceItem(
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
                self._sync_part_supplier(part.id, invoice.supplier_id, item_data.unit_price)
                self.stock_service.adjust_stock(part, item_data.quantity, StockMovementType.PURCHASE, invoice.id)
        self.db.refresh(invoice)
        return invoice

    def _sync_part_supplier(self, part_id: int, supplier_id: int, last_price: float) -> None:
        link = (
            self.db.query(PartSupplier)
            .filter(PartSupplier.part_id == part_id, PartSupplier.supplier_id == supplier_id)
            .first()
        )
        if link:
            link.last_purchase_price = last_price
        else:
            link = PartSupplier(
                part_id=part_id,
                supplier_id=supplier_id,
                last_purchase_price=last_price,
                is_preferred=False,
            )
            self.db.add(link)
