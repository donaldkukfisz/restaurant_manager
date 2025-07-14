from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from passlib.context import CryptContext

from database import Base, get_db, engine
from models import Reservation, User
from schema import NewReservation, AddUser, ReadUser

app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]
Base.metadata.create_all(bind=engine)





@app.get("/reservations")
async def read_all_reservations(db: db_dependency):
    return db.query(Reservation).all()

@app.get("/reservations/{reservation_id}")
async def read_single_reservation(reservation_id: int, db: db_dependency):
    single_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not single_reservation:
        return 'Reservation not found'
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