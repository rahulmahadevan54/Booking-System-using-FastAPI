from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, ValidationError, model_validator
from datetime import datetime

class UserCreate(BaseModel):
    user_id: int
    username: str
    password: str
    role: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Shows(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime
    capacity: int

    class Config:
        orm_mode = True


class ShowCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    capacity: int

    @model_validator(mode='before')
    def validate_time_order(cls, values):
        start = values.get('start_time')
        end = values.get('end_time')
        if start and end and end <= start:
            raise ValueError("end_time must be after start_time")
        return values



class ShowOut(Shows):
    pass

class ShowDeleteResponse(BaseModel):
    message: str

class ShowAttendeeCountResponse(BaseModel):
    message: str

class ShowAttendeeInfo(BaseModel):
    username: str
    user_id: int
    seat_id: int

class Seat(BaseModel):
    seat_id: int
    booked: bool
    show_id: int

    class Config:
        orm_mode = True

class SeatOut(BaseModel):
    show_id: int
    seat_id: int
    booked: bool
    user_id: Optional[int]

    class Config:
        orm_mode = True

class BookingResponse(BaseModel):
    message: str

class BookingInfo(BaseModel):
    show_id: int
    seat_id: int

class SeatInfo(BaseModel):
    seat_id: int
    show_id: int

class SeatCreateResponse(BaseModel):
    message: str
    seats: List[SeatInfo]
