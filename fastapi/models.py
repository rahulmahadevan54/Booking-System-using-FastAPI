from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role=Column(String,default='user')

class Show(Base):
    __tablename__ = 'shows'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    capacity = Column(Integer,default=200)

class Seat(Base):
    __tablename__ = 'seats'
    seat_id = Column(Integer, primary_key=True, index=True)
    booked = Column(Boolean)
    show_id = Column(Integer, ForeignKey("shows.id"))
    user_id=Column(Integer,ForeignKey("users.user_id"),nullable=True)
