from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import AddUser, ReadUser
from models import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


SECRET_KEY = "ae7a89c8aadb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def get_user_by_email(db: db_dependency, email: str):
    return db.query(User).filter(User.email == email).first()

@router.post("/register", response_model=ReadUser)
async def register(user_data:AddUser, db: db_dependency):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Taki użytkownik już istnieje.")
    hashed = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    return form_data.username
