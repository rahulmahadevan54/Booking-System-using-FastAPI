from pydantic import BaseModel
from datetime import datetime

class Shows(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime 
    capacity: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):  
    user_id: int
    username: str
    password: str  
    role:str

class UserResponse(BaseModel):  
    user_id: int
    username: str

    class Config:
        orm_mode = True

class Seat(BaseModel):
    seat_id: int
    booked: bool
    show_id: int

    class Config:
        orm_mode = True
class UserLogin(UserCreate):
    username:str
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
