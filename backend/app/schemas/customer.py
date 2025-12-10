from pydantic import BaseModel

from app.schemas.common import ORMBase


class CustomerBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    gst_number: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    notes: str | None = None
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    gst_number: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    notes: str | None = None
    is_active: bool | None = None


class CustomerOut(ORMBase, CustomerBase):
    id: int
