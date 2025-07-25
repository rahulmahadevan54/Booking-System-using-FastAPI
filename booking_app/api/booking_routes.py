# booking_app/routes/booking_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
import booking_app.core.oauth as oauth
from booking_app.schemas.schemas import SeatOut, BookingResponse, BookingInfo
from booking_app.services.booking_services import (
    get_available_seats_service,
    book_seat_service,
    view_user_bookings_service,
    view_my_bookings_service,
    cancel_booking_service
)

router = APIRouter()

@router.get('/availableseats/{show_id}', response_model=list[SeatOut])
def get_available_seats(show_id: int, db: Session = Depends(get_db)):
    return get_available_seats_service(show_id, db)


@router.post('/bookseats/{show_id}/{seat_id}', response_model=BookingResponse)
def book_seats(show_id: int, seat_id: int, db: Session = Depends(get_db),
               current_user: dict = Depends(oauth.get_current_user)):
    return book_seat_service(show_id, seat_id, current_user["user_id"], db)


@router.get('/users/{user_id}/bookings', response_model=list[BookingInfo])
def view_bookings(user_id: int, db: Session = Depends(get_db),
                  current_admin: dict = Depends(oauth.get_current_admin)):
    return view_user_bookings_service(user_id, db)


@router.get('/viewmybookings', response_model=list[SeatOut])
def view_my_bookings(db: Session = Depends(get_db),
                     current_user: dict = Depends(oauth.get_current_user)):
    return view_my_bookings_service(current_user["user_id"], db)


@router.post('/bookings/{show_id}/{seat_id}/cancel', response_model=BookingResponse)
def cancel_booking(show_id: int, seat_id: int, db: Session = Depends(get_db),
                   current_user: dict = Depends(oauth.get_current_user)):
    return cancel_booking_service(show_id, seat_id, current_user["user_id"], current_user["role"], db)
