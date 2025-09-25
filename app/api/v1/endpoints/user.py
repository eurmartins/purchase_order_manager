from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import create_user, get_user_by_email, get_user_by_username
from app.crud.user import get_user, get_users, update_user, delete_user
from app.db.session import SessionLocal
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import UserRole

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_users(db)

@router.post("/", response_model=UserRead)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return create_user(db, user)

@router.put("/{user_id}", response_model=UserRead)
def update_user_by_id(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user