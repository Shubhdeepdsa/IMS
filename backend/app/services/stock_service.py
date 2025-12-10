from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.part import Part
from app.models.stock_movement import StockMovement, StockMovementType


class StockService:
    def __init__(self, db: Session):
        self.db = db

    def adjust_stock(self, part: Part, quantity_change: int, movement_type: StockMovementType, source_id: int | None = None) -> None:
        new_stock = part.current_stock + quantity_change
        if new_stock < 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Insufficient stock for operation')
        part.current_stock = new_stock
        movement = StockMovement(
            part_id=part.id,
            movement_type=movement_type,
            source_id=source_id,
            quantity_change=quantity_change,
            balance_after=new_stock,
        )
        self.db.add(movement)
