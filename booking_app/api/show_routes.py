
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from booking_app.database.database import get_db
from booking_app.schemas.schemas import Shows, ShowOut, SeatCreateResponse, ShowDeleteResponse, ShowAttendeeCountResponse, ShowAttendeeInfo, ShowCreate
import booking_app.core.oauth as oauth

from booking_app.services.show_services import (
    create_show_service,
    get_all_shows_service,
    get_show_details_service,
    update_show_service,
    delete_show_service,
    count_attendees_service,
    get_attendees_service
)

router = APIRouter()


@router.post('/createshow', response_model=dict)
def create_show(show: ShowCreate, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    return create_show_service(show, db)


@router.get('/displayshows', response_model=list[dict])
def display_shows(db: Session = Depends(get_db)):
    return get_all_shows_service(db)


@router.get('/showdetails/{id}', response_model=ShowOut)
def show_details(id: int, db: Session = Depends(get_db)):
    return get_show_details_service(id, db)


@router.put('/show/{id}', response_model=ShowOut)
def update_show(id: int, show_data: Shows, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    return update_show_service(id, show_data, db)


@router.delete('/delete/{show_id}', response_model=ShowDeleteResponse)
def delete_show(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    return delete_show_service(show_id, db)


@router.get('/show/{show_id}/attendees/count', response_model=ShowAttendeeCountResponse)
def count(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    return count_attendees_service(show_id, db)


@router.get('/show/{show_id}/attendees', response_model=list[ShowAttendeeInfo])
def attendees(show_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(oauth.get_current_admin)):
    return get_attendees_service(show_id, db)
