from pydantic import BaseModel
from datetime import datetime
from app.enums.purchase_order_status import PurchaseOrderStatus


class PurchaseOrderSchemas:
    class PurchaseOrderBase(BaseModel):
        order_number: str
        assistant_id: int
        analyst_id: int
        status: PurchaseOrderStatus = PurchaseOrderStatus.PENDING
        total_amount: float
        notes: str | None = None

    class PurchaseOrderCreate(PurchaseOrderBase):
        pass

    class PurchaseOrderRead(PurchaseOrderBase):
        id: int
        created_at: datetime
        updated_at: datetime
        approved_at: datetime | None = None

        class Config:
            from_attributes = True

    class PurchaseOrderUpdate(BaseModel):
        order_number: str | None = None
        assistant_id: int | None = None
        analyst_id: int | None = None
        status: PurchaseOrderStatus | None = None
        total_amount: float | None = None
        notes: str | None = None
        approved_at: datetime | None = None
