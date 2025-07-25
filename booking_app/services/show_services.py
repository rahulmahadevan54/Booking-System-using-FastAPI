# booking_app/services/show_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from booking_app.models.models import Show, Seat, User
from booking_app.schemas.schemas import Shows, ShowCreate


def create_show_service(show: ShowCreate, db: Session):
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


def get_all_shows_service(db: Session):
    all_shows = db.query(Show).all()
    return [{a.id: a.title} for a in all_shows]


def get_show_details_service(show_id: int, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show


def update_show_service(show_id: int, show_data: Shows, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()

    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    old_capacity = show.capacity
    new_capacity = show_data.capacity

    show.title = show_data.title
    show.start_time = show_data.start_time
    show.end_time = show_data.end_time
    show.capacity = new_capacity

    print(f"Old: {old_capacity}, New: {new_capacity}")

    if new_capacity > old_capacity:
        for _ in range(new_capacity - old_capacity):
            seat = Seat(show_id=show.id,user_id=None,booked=False)
            db.add(seat)

    elif new_capacity < old_capacity:
        seats_to_delete = (
            db.query(Seat)
            .filter(Seat.show_id == show.id)
            .limit(old_capacity - new_capacity)
            .all()
        )
        for seat in seats_to_delete:
            db.delete(seat)

    db.commit()
    db.refresh(show)
    return show



def delete_show_service(show_id: int, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    seats = db.query(Seat).filter(Seat.show_id == show_id).all()
    for seat in seats:
        db.delete(seat)
    db.delete(show)
    db.commit()
    return {"message": "the show was deleted"}


def count_attendees_service(show_id: int, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == True).all()
    count = len(seats)
    return {"message": f"the total capacity of the show is {show.capacity} and the total booked seats is {count}"}


def get_attendees_service(show_id: int, db: Session):
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    seats = db.query(Seat).filter(Seat.show_id == show_id, Seat.booked == True).all()
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
