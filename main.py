from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

from routers.auth import hash_password
from database import Base, get_db, engine
from models import Reservation, User
from schema import NewReservation, AddUser, ReadUser
from routers import auth

app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)





@app.get("/reservations")
async def read_all_reservations(db: db_dependency):
    return db.query(Reservation).all()

@app.get("/reservations/{reservation_id}")
async def read_single_reservation(reservation_id: int, db: db_dependency):
    single_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not single_reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return single_reservation

@app.post("/reservations")
async def create_reservation(reservation: NewReservation, db: db_dependency):
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()

@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int, db: db_dependency):
    res_to_remove = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not res_to_remove:
        raise HTTPException(status_code=404, detail="Nie ma takiej rezerwacji!")
    db.query(Reservation).filter(Reservation.id == reservation_id).delete()
    db.commit()

@app.put("/reservations/{reservation_id}")
async def update_reservation(reservation_id: int, new_reservation: NewReservation, db: db_dependency):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Nie ma takiej rezerwacji!")
    else:
        reservation.first_name = new_reservation.first_name
        reservation.last_name = new_reservation.last_name
        reservation.number_of_people = new_reservation.number_of_people
        reservation.date = new_reservation.date
    db.commit()

@app.post("/users")
async def create_user(user: AddUser, db: db_dependency):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email,
                   hashed_password=hashed_password,
                   is_active=True,
                   is_admin=False)
    db.add(db_user)
    db.commit()

@app.get("/users/{email}")
async def find_user(db: db_dependency, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Nie ma takiego użytkownika!")
    return user


def get_user_by_email(db: db_dependency, email: str):
    return db.query(User).filter(User.email == email).first()

@app.get("/users")
async def read_all_users(db:db_dependency):
    users = db.query(User).all()
    return users

@app.post("/register", response_model=ReadUser)
def register(user_data: AddUser, db: db_dependency):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail='Taki użytkownik już istnieje!')
    hashed = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
