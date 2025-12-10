from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import ORMBase


class PurchaseInvoiceItemBase(BaseModel):
    part_id: int
    quantity: int
    unit_price: float
    discount_amount: float = 0
    tax_rate_percent: float
    tax_amount: float = 0
    line_total: float


class PurchaseInvoiceItemCreate(PurchaseInvoiceItemBase):
    pass


class PurchaseInvoiceItemOut(ORMBase, PurchaseInvoiceItemBase):
    id: int


class PurchaseInvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: date
    supplier_id: int
    subtotal: float
    total_tax: float
    total_amount: float
    payment_mode: str | None = None
    payment_status: str | None = None
    notes: str | None = None


class PurchaseInvoiceCreate(PurchaseInvoiceBase):
    items: list[PurchaseInvoiceItemCreate]


class PurchaseInvoiceOut(ORMBase, PurchaseInvoiceBase):
    id: int
    items: list[PurchaseInvoiceItemOut] = Field(default_factory=list)
