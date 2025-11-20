from fastapi import FastAPI

from ToDoApp import models
from ToDoApp.database import engine
from ToDoApp.routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
