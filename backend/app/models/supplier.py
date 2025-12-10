from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Supplier(Base):
    __tablename__ = 'suppliers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(255))
    gst_number: Mapped[str | None] = mapped_column(String(50))
    address_line1: Mapped[str | None] = mapped_column(String(255))
    address_line2: Mapped[str | None] = mapped_column(String(255))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    pincode: Mapped[str | None] = mapped_column(String(20))
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    parts = relationship('PartSupplier', back_populates='supplier', cascade='all, delete-orphan')
    purchase_invoices = relationship('PurchaseInvoice', back_populates='supplier')


class PartSupplier(Base):
    __tablename__ = 'part_suppliers'
    __table_args__ = (UniqueConstraint('part_id', 'supplier_id', name='uq_part_supplier'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id', ondelete='CASCADE'), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('suppliers.id', ondelete='CASCADE'), nullable=False)
    supplier_part_code: Mapped[str | None] = mapped_column(String(100))
    last_purchase_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    usual_lead_time_days: Mapped[int | None] = mapped_column(Integer)
    is_preferred: Mapped[bool] = mapped_column(Boolean, default=False)

    part = relationship('Part', back_populates='suppliers')
    supplier = relationship('Supplier', back_populates='parts')
