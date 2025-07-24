from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
from booking_app.models.models import Show, Seat, User
import booking_app.core.oauth as oauth
from booking_app.schemas.schemas import SeatOut,BookingResponse,BookingInfo

router = APIRouter()

@router.get('/availableseats/{show_id}', response_model=list[SeatOut])
def get_available_seats(show_id: int, db: Session = Depends(get_db)):

    show = db.query(Show).filter(Show.id == show_id).first()
    if show:
        nonbooked = []
        seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == False).all()
        for seat in seats:
            nonbooked.append(seat)
    return nonbooked

@router.post('/bookseats/{show_id}/{seat_id}', response_model=BookingResponse)
def book_seats(show_id: int, seat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth.get_current_user)):
    seat = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if seat.booked:
        raise HTTPException(status_code=400, detail="Seat already booked")
    
    seat.booked = True
    seat.user_id = current_user["user_id"]
    db.commit()
    db.refresh(seat)
    
    return {
        "message": f"Seat successfully booked for show {show_id}, seat no {seat_id}",
        "show_id": show_id,
        "seat_id": seat_id,
        "user_id": current_user["user_id"]
    }


@router.get('/users/{user_id}/bookings', response_model=list[BookingInfo])
def view_bookings(user_id: int, db: Session = Depends(get_db),current_admin: dict = Depends(oauth.get_current_admin)):
    user=db.query(User).filter(User.user_id==user_id).first()
    result=[]
    for seat in user.bookings:
        result.append({
            "show_id": seat.show_id,
            "seat_id": seat.seat_id
        })
    return result



@router.get('/viewmybookings', response_model=list[SeatOut])
def view_bookings(db: Session = Depends(get_db), current_user: dict = Depends(oauth.get_current_user)):
    user_id = current_user["user_id"]
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

@router.post('/bookings/{show_id}/{seat_id}/cancel', response_model=BookingResponse)
def free_seat(
    show_id: int,
    seat_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth.get_current_user)
):
    seat = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")

    if not seat.booked:
        raise HTTPException(status_code=400, detail="Seat is not booked")

    if current_user["role"] == "admin" or seat.user_id == current_user["user_id"]:
        seat.booked = False
        seat.user_id = None
        db.commit()
        return {"message": "Your booking has now been cancelled"}

    raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
