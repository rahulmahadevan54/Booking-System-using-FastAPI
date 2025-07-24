from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
from booking_app.schemas.schemas import Shows, ShowOut, SeatCreateResponse, ShowDeleteResponse, ShowAttendeeCountResponse, ShowAttendeeInfo,ShowCreate
from booking_app.models.models import Show, Seat
import booking_app.core.oauth as oauth

router = APIRouter()

@router.post('/createshow', response_model=dict)
def create_show(show: ShowCreate, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    new_show = Show(
        title=show.title,
        start_time=show.start_time,
        end_time=show.end_time,
        capacity=show.capacity
    )
    db.add(new_show)
    db.commit()
    db.refresh(new_show)

    seats = []
    for _ in range(new_show.capacity):
        seat = Seat(show_id=new_show.id, booked=False)
        db.add(seat)
        db.flush()
        seats.append({"seat_id": seat.seat_id, "show_id": seat.show_id})

    db.commit()

    return {"message": f"{len(seats)} seats created", "seats": seats}



@router.get('/displayshows', response_model=list[dict])
def display_shows(db: Session = Depends(get_db)):
    all_shows = db.query(Show).all()
    return [{a.id: a.title} for a in all_shows]


@router.get('/showdetails/{id}', response_model=ShowOut)
def show_details(id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show


@router.put('/show/{id}', response_model=ShowOut)
def update_show(id: int, show_data: Shows, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.id == id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    show.title = show_data.title
    show.start_time = show_data.start_time
    show.end_time = show_data.end_time
    show.capacity = show_data.capacity
    return show


@router.delete('/delete/{show_id}', response_model=ShowDeleteResponse)
def delete_show(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.show_id == show_id).first()
    seats = db.query(Seat).filter(Seat.show_id == show_id).all()
    for seat in seats:
        db.delete(seat)
    db.delete(show)
    return {"message": "the show was deleted"}


@router.get('/show/{show_id}/attendees/count', response_model=ShowAttendeeCountResponse)
def count(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.show_id == show_id).first()
    if show:
        seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == True).all()
        count = 0
        for seat in seats:
            count += 1
    return {"message": f"the total capacity of the show is {show.capacity} and the total booked seats is {count}"}


@router.get('/show/{show_id}/attendees', response_model=list[ShowAttendeeInfo])
def attendees(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == True).all()
    from booking_app.models.models import User
    details = []
    for seat in seats:
        user = db.query(User).filter(User.user_id == seat.user_id).first()
        if user:
            details.append({
                "username": user.username,
                "user_id": user.user_id,
                "seat_id": seat.seat_id
            })
    return details
