from pydantic import BaseModel
from datetime import datetime
from app.schemas.role import RoleSchemas


class UserSchemas:
    class UserBase(BaseModel):
        username: str
        email: str
        role_id: int

    class UserCreate(UserBase):
        password: str

    class UserRead(BaseModel):
        id: int
        username: str
        email: str
        role: RoleSchemas.RoleRead
        created_at: datetime
        updated_at: datetime

        class Config:
            from_attributes = True

    class UserUpdate(BaseModel):
        username: str | None = None
        email: str | None = None
        password: str | None = None
        role_id: int | None = None
