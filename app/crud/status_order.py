from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.status_order import StatusOrder
from app.schemas.status_order import StatusOrderSchemas


class StatusOrderCRUD:
    def __init__(self, db: Session, status_order_schemas=StatusOrderSchemas):
        self.db = db
        self.status_order_schemas = status_order_schemas

    def create_status_order(self, status_create: StatusOrderSchemas.StatusOrderCreate) -> StatusOrder:
        status = StatusOrder(name=status_create.name)
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def get_status_order(self, status_id: int) -> Optional[StatusOrder]:
        return self.db.query(StatusOrder).filter(StatusOrder.id == status_id).first()

    def get_status_orders(self) -> List[type[StatusOrder]]:
        return self.db.query(StatusOrder).all()

    def update_status_order(self, status_id: int, status_update: StatusOrderSchemas.StatusOrderBase) -> \
            (type[StatusOrder] | None):
        status = self.db.query(StatusOrder).filter(StatusOrder.id == status_id).first()
        if not status:
            return None
        status.name = status_update.name
        self.db.commit()
        self.db.refresh(status)
        return status

    def delete_status_order(self, status_id: int) -> bool:
        status = self.db.query(StatusOrder).filter(StatusOrder.id == status_id).first()
        if not status:
            return False
        self.db.delete(status)
        self.db.commit()
        return True
