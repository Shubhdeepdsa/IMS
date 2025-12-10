from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TractorModel(Base):
    __tablename__ = 'tractor_models'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    compatible_parts = relationship('PartCompatibleModel', back_populates='tractor_model', cascade='all, delete')


class PartCompatibleModel(Base):
    __tablename__ = 'parts_compatible_models'
    __table_args__ = (UniqueConstraint('part_id', 'tractor_model_id', name='uq_part_model'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.id', ondelete='CASCADE'), nullable=False)
    tractor_model_id: Mapped[int] = mapped_column(ForeignKey('tractor_models.id', ondelete='CASCADE'), nullable=False)

    part = relationship('Part', back_populates='compatible_models')
    tractor_model = relationship('TractorModel', back_populates='compatible_parts')
