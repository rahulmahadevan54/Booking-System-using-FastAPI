from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Show, Seat, User
import oauth

router = APIRouter()

@router.get('/availableseats/{show_id}')
def showavl(show_id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if show:
        nonbooked = []
        seats = db.query(Seat).filter(show_id == show_id, Seat.booked == False).all()
        for seat in seats:
            nonbooked.append(seat)
    return nonbooked

@router.post('/bookseats/{show_id}/{seat_id}')
def bookseats(show_id: int, seat_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth.get_current_user)):
    seat = db.query(Seat).filter(Seat.show_id == show_id, Seat.seat_id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if seat.booked:
        raise HTTPException(status_code=400, detail="Seat already booked")
    seat.booked = True
    seat.user_id = current_user["user_id"]
    db.commit()
    return {"message": f"Seat successfully booked for show {show_id}, seat no {seat_id}"}

@router.get('/users/{user_id}/bookings')
def view_bookings(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth.get_current_user)):
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    seats= db.query(Seat).filter(Seat.user_id == user_id).all()
    list=[]
    for seat in seats:
        list.append({"show_id":seat.show_id,"seat_id":seat.seat_id})
    return list



@router.get('/viewmybookings')
def view_bookings(db: Session = Depends(get_db), current_user: dict = Depends(oauth.get_current_user)):
    user_id = current_user["user_id"]
    seats = db.query(Seat).filter(Seat.user_id == user_id).all()
    bookings = []
    for seat in seats:
        bookings.append(seat)
    return bookings

@router.post('/bookings/{show_id}/{seat_id}/cancel')
def freeseat(show_id: int, seat_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin), current_user: dict = Depends(oauth.get_current_user)):
    seat = db.query(Seat).filter(show_id == show_id, seat_id == seat_id).first()
    if seat:
        if seat.booked:
            seat.user_id = None
            seat.booked = False
    db.commit()
    return {"message": "your booking has now been cancelled"}
