from enum import Enum as PyEnum

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PaymentMode(str, PyEnum):
    CASH = 'CASH'
    UPI = 'UPI'
    BANK = 'BANK'
    CREDIT = 'CREDIT'


class PaymentStatus(str, PyEnum):
    PAID = 'PAID'
    PARTIAL = 'PARTIAL'
    UNPAID = 'UNPAID'


class PurchaseInvoice(Base):
    __tablename__ = 'purchase_invoices'

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    invoice_date: Mapped[Date] = mapped_column(Date, nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id'), nullable=False)
    subtotal: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_tax: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    payment_mode: Mapped[str | None] = mapped_column(String(50))
    payment_status: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)

    supplier = relationship('Supplier', back_populates='purchase_invoices')
    items = relationship('PurchaseInvoiceItem', back_populates='invoice', cascade='all, delete-orphan')


class PurchaseInvoiceItem(Base):
    __tablename__ = 'purchase_invoice_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_invoice_id: Mapped[int] = mapped_column(ForeignKey('purchase_invoices.id', ondelete='CASCADE'), nullable=False)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    tax_rate_percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    line_total: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    invoice = relationship('PurchaseInvoice', back_populates='items')
    part = relationship('Part', back_populates='purchase_items')
