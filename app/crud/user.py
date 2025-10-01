from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSchemas
from app.core.security import get_password_hash


class UserCRUD:

    def __init__(self, db: Session, user_schemas=UserSchemas):
        self.db = db
        self.user_schemas = user_schemas

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: 'UserSchemas.UserCreate') -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=get_password_hash(user.password),
            role_id=user.role_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self) -> list[type[User]]:
        return self.db.query(User).all()

    def update_user(self, user_id: int, user_update: 'UserSchemas.UserUpdate') -> type[User] | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.password is not None:
            db_user.password_hash = get_password_hash(user_update.password)
        if user_update.role_id is not None:
            db_user.role_id = user_update.role_id

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> type[User] | None:
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user
