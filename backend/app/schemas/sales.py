from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import ORMBase


class SalesInvoiceItemBase(BaseModel):
    part_id: int
    quantity: int
    unit_price: float
    discount_amount: float = 0
    tax_rate_percent: float
    tax_amount: float = 0
    line_total: float


class SalesInvoiceItemCreate(SalesInvoiceItemBase):
    pass


class SalesInvoiceItemOut(ORMBase, SalesInvoiceItemBase):
    id: int


class SalesInvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: date
    customer_id: int | None = None
    subtotal: float
    total_tax: float
    total_amount: float
    payment_mode: str | None = None
    payment_status: str | None = None
    notes: str | None = None


class SalesInvoiceCreate(SalesInvoiceBase):
    items: list[SalesInvoiceItemCreate]


class SalesInvoiceOut(ORMBase, SalesInvoiceBase):
    id: int
    items: list[SalesInvoiceItemOut] = Field(default_factory=list)
