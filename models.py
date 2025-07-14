from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    number_of_people = Column(Integer)
    date = Column(DateTime)

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)