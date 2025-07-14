from datetime import datetime

from pydantic import BaseModel


class NewReservation(BaseModel):
    first_name: str
    last_name: str
    number_of_people: int
    date: datetime

class AddUser(BaseModel):
    email: str
    password: str

class ReadUser(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool