
from sqlalchemy.orm import Session
from fastapi import HTTPException
from booking_app.models.models import User
from booking_app.schemas.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_service(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.user_id == user.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already registered")

    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        user_id=user.user_id,
        username=user.username,
        hashed_password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
