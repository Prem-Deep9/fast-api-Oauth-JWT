from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ToDoApp.database import SessionLocal
from ToDoApp.models import Users

SECRET_KEY = "a8f3c9d1e7b6f4a2c5d8e9a1b7c3f6d4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not user.password == password:
        return False
    return user

def create_access_token(username:str, user_id:int, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {'sub': username, 'id':user_id, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {"username": username, "user_id": user_id}
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User") from exc

class CreateUserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = Users(**create_user_request.model_dump())
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    users =db.query(Users).all()
    return users
