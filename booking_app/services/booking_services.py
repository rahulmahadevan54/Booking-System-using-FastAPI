
from sqlalchemy.orm import Session
from fastapi import HTTPException
from booking_app.models.models import Show, Seat, User

def get_available_seats_service(show_id: int, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    return db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == False).all()


def book_seat_service(show_id: int, seat_id: int, user_id: int, db: Session):
    seat = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_id == seat_id).first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if seat.booked:
        raise HTTPException(status_code=400, detail="Seat already booked")

    seat.booked = True
    seat.user_id = user_id
    db.commit()
    db.refresh(seat)

    return {
        "message": f"Seat successfully booked for show {show_id}, seat no {seat_id}",
        "show_id": show_id,
        "seat_id": seat_id,
        "user_id": user_id
    }


def view_user_bookings_service(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [{"show_id": seat.show_id, "seat_id": seat.seat_id} for seat in user.bookings]


def view_my_bookings_service(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [
        {
            "show_id": seat.show_id,
            "seat_id": seat.seat_id,
            "booked": seat.booked,
            "user_id": seat.user_id
        }
        for seat in user.bookings
    ]


def cancel_booking_service(show_id: int, seat_id: int, user_id: int, role: str, db: Session):
    seat = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_id == seat_id).first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if not seat.booked:
        raise HTTPException(status_code=400, detail="Seat is not booked")

    if role == "admin" or seat.user_id == user_id:
        seat.booked = False
        seat.user_id = None
        db.commit()
        return {"message": "Your booking has now been cancelled"}

    raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
