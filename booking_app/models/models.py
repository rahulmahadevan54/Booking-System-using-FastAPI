from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from booking_app.database.database import Base

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)

    seats = relationship(
        "Seat",
        back_populates="show",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    bookings = relationship(
        "Seat",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Seat(Base):
    __tablename__ = "seats"
    seat_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    booked = Column(Boolean, default=False)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)

    show = relationship("Show", back_populates="seats")
    user = relationship("User", back_populates="bookings")
