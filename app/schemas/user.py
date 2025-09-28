from pydantic import BaseModel
from datetime import datetime
from app.enums.roles import UserRole


class UserSchemas:
    class UserBase(BaseModel):
        username: str
        email: str
        role: UserRole = UserRole.USER

    class UserCreate(UserBase):
        password: str

    class UserRead(UserBase):
        id: int
        created_at: datetime
        updated_at: datetime

        class Config:
            from_attributes = True

    class UserUpdate(BaseModel):
        username: str | None = None
        email: str | None = None
        password: str | None = None
        role: UserRole | None = None
