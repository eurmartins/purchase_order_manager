from fastapi import FastAPI
from app.api import router
from app.db.base import Base
from app.db.session import engine

#Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)