from pydantic import BaseModel
from datetime import datetime
from app.schemas.status_order import StatusOrderSchemas


class PurchaseOrderSchemas:
    class PurchaseOrderBase(BaseModel):
        order_number: str
        assistant_id: int
        analyst_id: int
        status_id: int
        total_amount: float
        notes: str | None = None

    class PurchaseOrderCreate(PurchaseOrderBase):
        pass

    class PurchaseOrderRead(BaseModel):
        id: int
        order_number: str
        assistant_id: int
        analyst_id: int
        status: StatusOrderSchemas.StatusOrderRead
        total_amount: float
        notes: str | None = None
        created_at: datetime
        updated_at: datetime
        approved_at: datetime | None = None

        class Config:
            from_attributes = True

    class PurchaseOrderUpdate(BaseModel):
        order_number: str | None = None
        assistant_id: int | None = None
        analyst_id: int | None = None
        status_id: int | None = None
        total_amount: float | None = None
        notes: str | None = None
        approved_at: datetime | None = None
