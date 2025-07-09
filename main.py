from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import FastAPI, Depends
from typing import Annotated

SQLALCHEMY_DATABASE_URL = 'sqlite:///./reservation_base.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    number_of_people = Column(Integer)
    date = Column(DateTime)

Base.metadata.create_all(bind=engine)

@app.get("/reservations")
def read_all_reservations(db: db_dependency):
    return db.query(Reservation).all()

@app.get("/reservations/{reservation_id}")
def read_single_reservation(reservation_id: int, db: db_dependency):
    single_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not single_reservation:
        return 'Reservation not found'
    return single_reservation



