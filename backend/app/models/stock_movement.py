from enum import Enum as PyEnum

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class StockMovementType(str, PyEnum):
    PURCHASE = 'PURCHASE'
    SALE = 'SALE'
    ADJUSTMENT = 'ADJUSTMENT'


class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id'), nullable=False)
    movement_type: Mapped[StockMovementType] = mapped_column(Enum(StockMovementType), nullable=False)
    source_id: Mapped[int | None] = mapped_column(Integer)
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)

    part = relationship('Part', back_populates='stock_movements')
