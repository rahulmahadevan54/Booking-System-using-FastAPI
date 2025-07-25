from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
from booking_app.schemas.schemas import UserCreate, UserResponse
from booking_app.services.user_services import create_user_service

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)
