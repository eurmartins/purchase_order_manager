from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.role import RoleSchemas
from app.crud.role import RoleCRUD
from app.api.v1.endpoints.auth import AuthController
from app.db.dependencies import get_db

router = APIRouter()
auth_controller = AuthController()
get_current_user = auth_controller.get_current_user

class RoleController:
    def __init__(self, role_crud_class=RoleCRUD):
        self.role_crud_class = role_crud_class

    def read_role(self, role_id: int, db: Session, current_user):
        role_crud = self.role_crud_class(db)
        db_role = role_crud.get_role(role_id)
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return db_role

    def read_roles(self, db: Session, current_user):
        role_crud = self.role_crud_class(db)
        return role_crud.get_roles()

    def create_new_role(self, role: RoleSchemas.RoleCreate, db: Session, current_user):
        role_crud = self.role_crud_class(db)
        return role_crud.create_role(role)

    def update_role_by_id(self, role_id: int, role: RoleSchemas.RoleBase, db: Session, current_user):
        role_crud = self.role_crud_class(db)
        db_role = role_crud.update_role(role_id, role)
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return db_role

    def delete_role_by_id(self, role_id: int, db: Session, current_user):
        role_crud = self.role_crud_class(db)
        db_role = role_crud.delete_role(role_id)
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")
        return db_role

role_controller = RoleController()

@router.get("/{role_id}", response_model=RoleSchemas.RoleRead)
def read_role(role_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return role_controller.read_role(role_id, db, current_user)

@router.get("/", response_model=list[RoleSchemas.RoleRead])
def read_roles(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return role_controller.read_roles(db, current_user)

@router.post("/", response_model=RoleSchemas.RoleRead)
def create_new_role(role: RoleSchemas.RoleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return role_controller.create_new_role(role, db, current_user)

@router.put("/{role_id}", response_model=RoleSchemas.RoleRead)
def update_role_by_id(role_id: int, role: RoleSchemas.RoleBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return role_controller.update_role_by_id(role_id, role, db, current_user)

@router.delete("/{role_id}", response_model=RoleSchemas.RoleRead)
def delete_role_by_id(role_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return role_controller.delete_role_by_id(role_id, db, current_user)

