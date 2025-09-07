from fastapi import FastAPI
from app.api import router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)