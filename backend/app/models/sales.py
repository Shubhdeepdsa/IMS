from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SalesInvoice(Base):
    __tablename__ = 'sales_invoices'

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    invoice_date: Mapped[Date] = mapped_column(Date, nullable=False)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customers.id'))
    subtotal: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_tax: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    payment_mode: Mapped[str | None] = mapped_column(String(50))
    payment_status: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)

    customer = relationship('Customer', back_populates='sales_invoices')
    items = relationship('SalesInvoiceItem', back_populates='invoice', cascade='all, delete-orphan')


class SalesInvoiceItem(Base):
    __tablename__ = 'sales_invoice_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    sales_invoice_id: Mapped[int] = mapped_column(ForeignKey('sales_invoices.id', ondelete='CASCADE'), nullable=False)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    tax_rate_percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    line_total: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    invoice = relationship('SalesInvoice', back_populates='items')
    part = relationship('Part', back_populates='sales_items')
