from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_admin
from app.db.session import get_db
from app.models.tractor_model import TractorModel
from app.schemas.tractor_model import TractorModelCreate, TractorModelOut, TractorModelUpdate

router = APIRouter()


@router.get('/', response_model=list[TractorModelOut])
def list_models(db: Session = Depends(get_db), limit: int = Query(50, le=100), offset: int = 0):
    return db.query(TractorModel).offset(offset).limit(limit).all()


@router.get('/{model_id}', response_model=TractorModelOut)
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.get(TractorModel, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tractor model not found')
    return model


@router.post('/', response_model=TractorModelOut, dependencies=[Depends(get_current_active_admin)])
def create_model(model_in: TractorModelCreate, db: Session = Depends(get_db)):
    model = TractorModel(**model_in.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.put('/{model_id}', response_model=TractorModelOut, dependencies=[Depends(get_current_active_admin)])
def update_model(model_id: int, model_in: TractorModelUpdate, db: Session = Depends(get_db)):
    model = db.get(TractorModel, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tractor model not found')
    for field, value in model_in.dict(exclude_unset=True).items():
        setattr(model, field, value)
    db.commit()
    db.refresh(model)
    return model


@router.delete('/{model_id}', response_model=TractorModelOut, dependencies=[Depends(get_current_active_admin)])
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.get(TractorModel, model_id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tractor model not found')
    model.is_active = False
    db.commit()
    db.refresh(model)
    return model
