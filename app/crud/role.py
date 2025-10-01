from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleSchemas
from typing import Optional


class RoleCRUD:

    def __init__(self, db: Session, role_schemas=RoleSchemas):
        self.db = db
        self.role_schemas = role_schemas

    def create_role(self, role_create: RoleSchemas.RoleCreate) -> Role:
        role = Role(name=role_create.name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_role(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_roles(self) -> list[type[Role]]:
        return self.db.query(Role).all()

    def update_role(self, role_id: int, role_update: RoleSchemas.RoleBase) -> type[Role] | None:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        role.name = role_update.name
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete_role(self, role_id: int) -> bool:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return False
        self.db.delete(role)
        self.db.commit()
        return True
