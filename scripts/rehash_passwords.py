# Script para re-hash de senhas em texto puro no banco de dados

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.user import User
from app.core.security import get_password_hash

# Substitua pela sua string de conexão real
DATABASE_URL = "mysql+pymysql://usuario:senha@localhost:3306/seubanco"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

users = session.query(User).all()
for user in users:

    if not user.password_hash.startswith("$2b$"):
        user.password_hash = get_password_hash(user.password_hash)
        print(f"Senha do usuário {user.username} atualizada.")

session.commit()
session.close()

