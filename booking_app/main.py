from fastapi import FastAPI
from booking_app.api import user_routes, show_routes, booking_routes
import booking_app.core.auth as auth
from booking_app.database.database import Base, engine
from booking_app.models.models import Show, User, Seat  
from booking_app.core.init_db import init_db

app = FastAPI()
@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(auth.router)



app.include_router(user_routes.router, tags=["User"])
app.include_router(show_routes.router, tags=["Show"])
app.include_router(booking_routes.router, tags=["Booking"])
