from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.purchase_orders import PurchaseOrderSchemas
from app.crud.purchase_orders import PurchaseOrderCRUD
from app.api.v1.endpoints.auth import AuthController
from app.db.dependencies import get_db

router = APIRouter()
auth_controller = AuthController()
get_current_user = auth_controller.get_current_user


class PurchaseOrderController:
    def __init__(self, purchase_order_crud=PurchaseOrderCRUD):
        self.purchase_order_crud_class = purchase_order_crud

    def read_purchase_order(self, order_id: int, db: Session, current_user):
        purchase_order_crud = self.purchase_order_crud_class(db)
        db_order = purchase_order_crud.get_purchase_order(order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return db_order

    def read_purchase_orders(self, db: Session, current_user):
        purchase_order_crud = self.purchase_order_crud_class(db)
        return purchase_order_crud.get_purchase_orders()

    def create_new_purchase_order(self, order: PurchaseOrderSchemas.PurchaseOrderCreate, db: Session, current_user):
        purchase_order_crud = self.purchase_order_crud_class(db)
        return purchase_order_crud.create_purchase_order(order)

    def update_purchase_order_by_id(self, order_id: int, order: PurchaseOrderSchemas.PurchaseOrderUpdate, db: Session,
                                    current_user):
        purchase_order_crud = self.purchase_order_crud_class(db)
        db_order = purchase_order_crud.update_purchase_order(order_id, order)
        if not db_order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return db_order

    def delete_purchase_order_by_id(self, order_id: int, db: Session, current_user):
        purchase_order_crud = self.purchase_order_crud_class(db)
        db_order = purchase_order_crud.delete_purchase_order(order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return db_order


purchase_order_controller = PurchaseOrderController()


@router.get("/{order_id}", response_model=PurchaseOrderSchemas.PurchaseOrderRead)
def read_purchase_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return purchase_order_controller.read_purchase_order(order_id, db, current_user)


@router.get("/", response_model=list[PurchaseOrderSchemas.PurchaseOrderRead])
def read_purchase_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return purchase_order_controller.read_purchase_orders(db, current_user)


@router.post("/", response_model=PurchaseOrderSchemas.PurchaseOrderRead)
def create_new_purchase_order(order: PurchaseOrderSchemas.PurchaseOrderCreate, db: Session = Depends(get_db),
                              current_user=Depends(get_current_user)):
    return purchase_order_controller.create_new_purchase_order(order, db, current_user)


@router.put("/{order_id}", response_model=PurchaseOrderSchemas.PurchaseOrderRead)
def update_purchase_order_by_id(order_id: int, order: PurchaseOrderSchemas.PurchaseOrderUpdate,
                                db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return purchase_order_controller.update_purchase_order_by_id(order_id, order, db, current_user)


@router.delete("/{order_id}", response_model=PurchaseOrderSchemas.PurchaseOrderRead)
def delete_purchase_order_by_id(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return purchase_order_controller.delete_purchase_order_by_id(order_id, db, current_user)
