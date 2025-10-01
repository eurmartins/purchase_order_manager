from datetime import datetime
from pydantic import BaseModel


class StatusOrderSchemas:
    class StatusOrderBase(BaseModel):
        name: str

    class StatusOrderCreate(StatusOrderBase):
        pass

    class StatusOrderRead(StatusOrderBase):
        id: int
        created_at: datetime
        updated_at: datetime

        class Config:
            from_attributes = True