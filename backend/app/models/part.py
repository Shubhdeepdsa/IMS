from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Part(Base):
    __tablename__ = 'parts'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey('part_categories.id'))
    unit_of_measure: Mapped[str | None] = mapped_column(String(50))
    purchase_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    selling_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    mrp: Mapped[float | None] = mapped_column(Numeric(12, 2))
    tax_rate_percent: Mapped[float | None] = mapped_column(Numeric(5, 2))
    min_stock_level: Mapped[int] = mapped_column(Integer, default=0)
    current_stock: Mapped[int] = mapped_column(Integer, default=0)
    location_rack: Mapped[str | None] = mapped_column(String(50))
    location_shelf: Mapped[str | None] = mapped_column(String(50))
    location_box: Mapped[str | None] = mapped_column(String(50))
    primary_supplier_id: Mapped[int | None] = mapped_column(ForeignKey('suppliers.id'))
    barcode_value: Mapped[str | None] = mapped_column(String(255), unique=True)
    image_url: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category = relationship('PartCategory', back_populates='parts')
    suppliers = relationship('PartSupplier', back_populates='part', cascade='all, delete-orphan')
    compatible_models = relationship('PartCompatibleModel', back_populates='part', cascade='all, delete-orphan')
    purchase_items = relationship('PurchaseInvoiceItem', back_populates='part')
    sales_items = relationship('SalesInvoiceItem', back_populates='part')
    stock_adjustments = relationship('StockAdjustment', back_populates='part')
    stock_movements = relationship('StockMovement', back_populates='part')
