from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True