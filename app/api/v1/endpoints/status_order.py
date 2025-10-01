from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.status_order import StatusOrderSchemas
from app.crud.status_order import StatusOrderCRUD
from app.api.v1.endpoints.auth import get_current_user
from app.db.dependencies import get_db

router = APIRouter()

class StatusOrderController:
    def __init__(self, crud_class=StatusOrderCRUD):
        self.crud_class = crud_class

    def read_status_order(self, status_id: int, db: Session):
        crud = self.crud_class(db)
        status = crud.get_status_order(status_id)
        if not status:
            raise HTTPException(status_code=404, detail="StatusOrder not found")
        return status

    def read_status_orders(self, db: Session):
        crud = self.crud_class(db)
        return crud.get_status_orders()

    def create_status_order(self, status: StatusOrderSchemas.StatusOrderCreate, db: Session):
        crud = self.crud_class(db)
        return crud.create_status_order(status)

    def update_status_order(self, status_id: int, status: StatusOrderSchemas.StatusOrderBase, db: Session):
        crud = self.crud_class(db)
        updated = crud.update_status_order(status_id, status)
        if not updated:
            raise HTTPException(status_code=404, detail="StatusOrder not found")
        return updated

    def delete_status_order(self, status_id: int, db: Session):
        crud = self.crud_class(db)
        deleted = crud.delete_status_order(status_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatusOrder not found")
        return deleted

controller = StatusOrderController()

@router.get("/{status_id}", response_model=StatusOrderSchemas.StatusOrderRead)
def read_status_order(status_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return controller.read_status_order(status_id, db)

@router.get("/", response_model=list[StatusOrderSchemas.StatusOrderRead])
def read_status_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return controller.read_status_orders(db)

@router.post("/", response_model=StatusOrderSchemas.StatusOrderRead)
def create_status_order(status: StatusOrderSchemas.StatusOrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return controller.create_status_order(status, db)

@router.put("/{status_id}", response_model=StatusOrderSchemas.StatusOrderRead)
def update_status_order(status_id: int, status: StatusOrderSchemas.StatusOrderBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return controller.update_status_order(status_id, status, db)

@router.delete("/{status_id}", response_model=bool)
def delete_status_order(status_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return controller.delete_status_order(status_id, db)
