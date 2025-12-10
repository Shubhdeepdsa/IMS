from pydantic import BaseModel

from app.schemas.common import ORMBase


class StockAdjustmentBase(BaseModel):
    part_id: int
    adjustment_type: str
    quantity_change: int
    reason: str | None = None


class StockAdjustmentCreate(StockAdjustmentBase):
    pass


class StockAdjustmentOut(ORMBase, StockAdjustmentBase):
    id: int
    created_by_user_id: int


class StockMovementBase(BaseModel):
    part_id: int
    movement_type: str
    source_id: int | None = None
    quantity_change: int
    balance_after: int


class StockMovementOut(ORMBase, StockMovementBase):
    id: int
