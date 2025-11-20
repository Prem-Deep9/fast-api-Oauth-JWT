from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, db: db_dependency):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    todo_model = Todos(**todo_request.model_dump(), user_id=user.get("id"))
    db.add(todo_model)
    db.commit()
