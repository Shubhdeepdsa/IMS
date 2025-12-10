from pydantic import BaseModel

from app.schemas.common import ORMBase


class PartSupplierLink(BaseModel):
    supplier_id: int
    supplier_part_code: str | None = None
    last_purchase_price: float | None = None
    usual_lead_time_days: int | None = None
    is_preferred: bool = False


class PartBase(BaseModel):
    part_code: str
    name: str
    category_id: int | None = None
    unit_of_measure: str | None = None
    purchase_price: float | None = None
    selling_price: float | None = None
    mrp: float | None = None
    tax_rate_percent: float | None = None
    min_stock_level: int = 0
    current_stock: int = 0
    location_rack: str | None = None
    location_shelf: str | None = None
    location_box: str | None = None
    primary_supplier_id: int | None = None
    barcode_value: str | None = None
    image_url: str | None = None
    notes: str | None = None
    is_active: bool = True


class PartCreate(PartBase):
    suppliers: list[PartSupplierLink] | None = None


class PartUpdate(BaseModel):
    part_code: str | None = None
    name: str | None = None
    category_id: int | None = None
    unit_of_measure: str | None = None
    purchase_price: float | None = None
    selling_price: float | None = None
    mrp: float | None = None
    tax_rate_percent: float | None = None
    min_stock_level: int | None = None
    current_stock: int | None = None
    location_rack: str | None = None
    location_shelf: str | None = None
    location_box: str | None = None
    primary_supplier_id: int | None = None
    barcode_value: str | None = None
    image_url: str | None = None
    notes: str | None = None
    is_active: bool | None = None


class PartOut(ORMBase, PartBase):
    id: int


class PartSupplierOut(ORMBase, PartSupplierLink):
    id: int
    part_id: int


class PartSupplierPayload(BaseModel):
    supplier_part_code: str | None = None
    last_purchase_price: float | None = None
    usual_lead_time_days: int | None = None
    is_preferred: bool = False


class PartCompatibilityCreate(BaseModel):
    tractor_model_id: int


class PartCompatibilityOut(ORMBase):
    id: int
    part_id: int
    tractor_model_id: int
