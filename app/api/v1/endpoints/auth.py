from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.auth import JWTSchemas
from app.schemas.user import UserSchemas
from app.crud.user import UserCRUD
from app.core.security import verify_password, create_access_token, verify_token
from app.core.config import settings
from app.db.dependencies import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


class AuthController:
    def __init__(self, user_crud_class=UserCRUD):
        self.user_crud_class = user_crud_class

    def authenticate_user(self, db: Session, username: str, password: str):
        user_crud = self.user_crud_class(db)
        user = user_crud.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user

    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        username = verify_token(token)
        if username is None:
            raise credentials_exception
        user_crud = self.user_crud_class(db)
        user = user_crud.get_user_by_username(username=username)
        if user is None:
            raise credentials_exception
        return user

    def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = self.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


auth_controller = AuthController()


@router.post("/login", response_model=JWTSchemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_controller.login_for_access_token(form_data, db)


@router.get("/me", response_model=UserSchemas.UserRead)
def read_users_me(current_user: UserSchemas.UserRead = Depends(AuthController().get_current_user)):
    return current_user