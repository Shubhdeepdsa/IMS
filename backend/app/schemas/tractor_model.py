from pydantic import BaseModel

from app.schemas.common import ORMBase


class TractorModelBase(BaseModel):
    brand: str
    model_name: str
    description: str | None = None
    is_active: bool = True


class TractorModelCreate(TractorModelBase):
    pass


class TractorModelUpdate(BaseModel):
    brand: str | None = None
    model_name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TractorModelOut(TractorModelBase, ORMBase):
    id: int
