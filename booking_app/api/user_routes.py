from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
from booking_app.schemas.schemas import UserCreate, UserResponse
from booking_app.models.models import User
from passlib.context import CryptContext
import booking_app.core.oauth as oauth

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = str(pwd_context.hash(user.password))
    db_user = User(user_id=user.user_id, username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(db_user)
    return db_user
