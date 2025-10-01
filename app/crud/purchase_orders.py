from sqlalchemy.orm import Session
from app.models.purchase_orders import PurchaseOrder
from app.schemas.purchase_orders import PurchaseOrderSchemas


class PurchaseOrderCRUD:

    def __init__(self, db: Session, purchase_order_schemas=PurchaseOrderSchemas):
        self.db = db
        self.purchase_order_schemas = purchase_order_schemas

    def get_purchase_order(self, order_id: int):
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

    def get_purchase_orders(self):
        return self.db.query(PurchaseOrder).all()

    def create_purchase_order(self, order: 'PurchaseOrderSchemas.PurchaseOrderCreate'):
        db_order = PurchaseOrder(
            order_number=order.order_number,
            assistant_id=order.assistant_id,
            analyst_id=order.analyst_id,
            status_id=order.status_id,
            total_amount=order.total_amount,
            notes=order.notes
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def update_purchase_order(self, order_id: int, order_update: 'PurchaseOrderSchemas.PurchaseOrderUpdate'):
        db_order = self.get_purchase_order(order_id)
        if not db_order:
            return None
        update_data = order_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def delete_purchase_order(self, order_id: int):
        db_order = self.get_purchase_order(order_id)
        if not db_order:
            return None
        self.db.delete(db_order)
        self.db.commit()
        return db_order
