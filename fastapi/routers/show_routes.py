from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import Shows
from models import Show, Seat
import oauth

router = APIRouter()

@router.post('/addshow', response_model=None)
def addshow(show: Shows, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    new_show = Show(
        id=show.id,
        title=show.title,
        start_time=show.start_time,
        end_time=show.end_time,
        capacity=show.capacity
    )
    db.add(new_show)
    db.commit()
    show = db.query(Show).filter(Show.id == new_show.id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    existing_seat = db.query(Seat).filter(Seat.show_id == new_show.id).first()
    if existing_seat:
        raise HTTPException(status_code=400, detail="Seats already created for this show.")

    seats = []
    for _ in range(show.capacity):
        seat = Seat(show_id=show.id, booked=False)
        db.add(seat)
        db.flush()
        seats.append({"seat_id": seat.seat_id, "show_id": seat.show_id})
    db.commit()
    db.refresh(new_show)
    db.commit()

    return {"message": f"{len(seats)} seats created", "seats": seats}

@router.get('/shows')
def shows(db: Session = Depends(get_db)):
    all_shows = db.query(Show).all()
    return [{a.id: a.title} for a in all_shows]

@router.get('/show/{id}', response_model=Shows)
def showbyid(id: int, db: Session = Depends(get_db)):
    show = db.query(Show).filter(Show.id == id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

@router.put('/show/{id}', response_model=Shows)
def update_show(id: int, show_data: Shows, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.id == id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    show.title = show_data.title
    show.start_time = show_data.start_time
    show.end_time = show_data.end_time
    show.capacity = show_data.capacity
    db.commit()
    db.refresh(show)
    return show

@router.delete('/{show_id}/delete')
def deleteshow(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(show_id == show_id).first()
    seats=db.query(Seat).filter(show_id==show_id).all()
    for seat in seats:
        db.delete(seat)
    db.delete(show)
    db.commit()
    return {"message": "the show was deleted"}

@router.get('/show/{show_id}/attendees/count')
def ratio(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(show_id == show_id).first()
    if show:
        seats = db.query(Seat).filter(show_id == show_id, Seat.booked == True).all()
        count = 0
        for seat in seats:
            count += 1
    return {"message": f"the total capacity of the show is {show.capacity} and the total booked seats is {count}"}

@router.get('/show/{show_id}/attendees')
def attendees(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == True).all()
    from models import User
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
