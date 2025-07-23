from fastapi import FastAPI
from routers import user_routes, show_routes, booking_routes
import auth
app = FastAPI()
from database import Base, engine
from models import Show, User, Seat  

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)



app.include_router(user_routes.router, tags=["User"])
app.include_router(show_routes.router, tags=["Show"])
app.include_router(booking_routes.router, tags=["Booking"])
