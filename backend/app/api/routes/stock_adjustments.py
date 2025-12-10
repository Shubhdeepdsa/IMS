from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.part import Part
from app.models.stock_adjustment import StockAdjustment
from app.models.stock_movement import StockMovementType
from app.schemas.stock import StockAdjustmentCreate, StockAdjustmentOut
from app.services.stock_service import StockService

router = APIRouter()


@router.get('/', response_model=list[StockAdjustmentOut])
def list_adjustments(db: Session = Depends(get_db), limit: int = Query(50, le=100), offset: int = 0):
    return db.query(StockAdjustment).offset(offset).limit(limit).all()


@router.post('/', response_model=StockAdjustmentOut)
def create_adjustment(
    adjustment_in: StockAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_admin),
):
    part = db.get(Part, adjustment_in.part_id)
    if not part:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Part not found')
    stock_service = StockService(db)
    adjustment = StockAdjustment(
        part_id=adjustment_in.part_id,
        adjustment_type=adjustment_in.adjustment_type,
        quantity_change=adjustment_in.quantity_change,
        reason=adjustment_in.reason,
        created_by_user_id=current_user.id,
    )
    with db.begin():
        db.add(adjustment)
        db.flush()
        movement_type = StockMovementType.ADJUSTMENT
        stock_service.adjust_stock(part, adjustment.quantity_change, movement_type, source_id=adjustment.id)
    db.refresh(adjustment)
    return adjustment
