from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserSchemas
from app.crud.user import UserCRUD
from app.api.v1.endpoints.auth import get_current_user
from app.db.dependencies import get_db

router = APIRouter()


class UserController:
    def __init__(self, user_crud=UserCRUD):
        self.user_crud_class = user_crud

    def read_user(self, user_id: int, db: Session, current_user: UserSchemas.UserRead):
        user_crud = self.user_crud_class(db)
        db_user = user_crud.get_user(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def read_users(self, db: Session, current_user: UserSchemas.UserRead):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        user_crud = self.user_crud_class(db)
        return user_crud.get_users()

    def create_new_user(self, user: UserSchemas.UserCreate, db: Session):
        user_crud = self.user_crud_class(db)
        if user_crud.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if user_crud.get_user_by_username(user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        return user_crud.create_user(user)

    def update_user_by_id(self, user_id: int, user: UserSchemas.UserUpdate, db: Session,
                            current_user: UserSchemas.UserRead):
        if current_user.id != user_id and current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        user_crud = self.user_crud_class(db)
        db_user = user_crud.update_user(user_id, user)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def delete_user_by_id(self, user_id: int, db: Session, current_user: UserSchemas.UserRead):
        if current_user.role.name != "ADMIN":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        user_crud = self.user_crud_class(db)
        db_user = user_crud.delete_user(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


user_controller = UserController()


@router.get("/{user_id}", response_model=UserSchemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db),
                current_user: UserSchemas.UserRead = Depends(get_current_user)):
    return user_controller.read_user(user_id, db, current_user)


@router.get("/", response_model=list[UserSchemas.UserRead])
def read_users(db: Session = Depends(get_db), current_user: UserSchemas.UserRead = Depends(get_current_user)):
    return user_controller.read_users(db, current_user)


@router.post("/", response_model=UserSchemas.UserRead)
def create_new_user(user: UserSchemas.UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_new_user(user, db)


@router.put("/{user_id}", response_model=UserSchemas.UserRead)
def update_user_by_id(user_id: int, user: UserSchemas.UserUpdate, db: Session = Depends(get_db),
                        current_user: UserSchemas.UserRead = Depends(get_current_user)):
    return user_controller.update_user_by_id(user_id, user, db, current_user)


@router.delete("/{user_id}", response_model=UserSchemas.UserRead)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db),
                        current_user: UserSchemas.UserRead = Depends(get_current_user)):
    return user_controller.delete_user_by_id(user_id, db, current_user)
