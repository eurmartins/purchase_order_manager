from datetime import datetime
from pydantic import BaseModel


class RoleSchemas:
    class RoleBase(BaseModel):
        name: str

    class RoleCreate(RoleBase):
        pass

    class RoleRead(RoleBase):
        id: int
        created_at: datetime
        updated_at: datetime

        class Config:
            from_attributes = True
