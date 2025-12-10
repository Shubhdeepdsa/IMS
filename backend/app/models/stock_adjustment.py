from enum import Enum as PyEnum

from sqlalchemy import Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AdjustmentType(str, PyEnum):
    DAMAGE = 'DAMAGE'
    CUSTOMER_RETURN = 'CUSTOMER_RETURN'
    SUPPLIER_RETURN = 'SUPPLIER_RETURN'
    MANUAL_CORRECTION = 'MANUAL_CORRECTION'


class StockAdjustment(Base):
    __tablename__ = 'stock_adjustments'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id'), nullable=False)
    adjustment_type: Mapped[AdjustmentType] = mapped_column(Enum(AdjustmentType), nullable=False)
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    part = relationship('Part', back_populates='stock_adjustments')
