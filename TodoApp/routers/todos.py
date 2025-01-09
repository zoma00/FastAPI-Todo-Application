import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from .auth import get_current_user

from models import Todos, Users  # Ensure Users model is imported
from routers.auth import hash_password, PasswordReset

logging.basicConfig ()
logging.getLogger ('sqlalchemy.engine').setLevel (logging.INFO)


router = APIRouter ()


# Dependency to get the database session
def get_db ():
    db = SessionLocal ()
    try:
        yield db
    finally:
        db.close ()


# Dependency annotation
db_dependency = Annotated[Session, Depends (get_db)]
user_dependency = Annotated[dict, Depends (get_current_user)]


# Pydantic model for requests
class TodoRequest (BaseModel):
    title: str = Field (min_length=3)
    description: str = Field (min_length=3, max_length=100)
    priority: int = Field (gt=0, lt=6)
    complete: bool


# Route to get all todos
@router.get ("/", status_code=status.HTTP_200_OK)
async def read_all (user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException (status_code=401, detail='Authentication Failed')
    return db.query (Todos).filter (Todos.owner_id == user.get ('id')).all ()


# Route to get a specific todo by its ID
@router.get ("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo (user: user_dependency, db: db_dependency, todo_id: int = Path (gt=0)):
    if user is None:
        raise HTTPException (status_code=401, detail='Authentication Failed')

    todo_model = db.query (Todos).filter (Todos.id == todo_id) \
        .filter (Todos.owner_id == user.get ('id')).first ()
    if todo_model is not None:
        return todo_model
    raise HTTPException (status_code=404, detail="Todo not found")


# Route to create a new todo
@router.post ("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo (user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException (status_code=401, detail='Authentication Failed')
    todo_model = Todos (**todo_request.dict (), owner_id=user.get ('id'))
    db.add (todo_model)
    db.commit ()


# return todo_model  # Optionally return the created todo


# Route to update a todo by ID
@router.put ("/todo/{todo_id}", response_model=TodoRequest, status_code=status.HTTP_200_OK)
async def update_todo (user: user_dependency, db: db_dependency,
                       todo_request: TodoRequest,
                       todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException (status_code=401, detail='Authentication Failed')

    todo_model = db.query (Todos).filter (Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first ()
    if todo_model is None:
        raise HTTPException (status_code=404, detail="Todo not found.")

    # Update the todo record with new data
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.commit ()

    return todo_model  # Return the updated todo


# Route to delete a todo by ID
@router.delete ("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo (user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException (status_code=404, detail="Todo not found.")

    todo_model = db.query (Todos).filter (Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first ()
    if todo_model is None:
        raise HTTPException (status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id) .filter(Todos.owner_id == user.get('id')).delete()
    db.delete (todo_model)

    db.commit ()


# Route to reset password
@router.post ("/reset-password/")
async def reset_password (reset: PasswordReset, db: db_dependency):
    hashed_password = hash_password (reset.new_password)

    # Find the user in the database
    user = db.query (Users).filter (Users.username == reset.username).first ()
    if user is None:
        raise HTTPException (status_code=404, detail="User not found")

    # Update the user's password
    user.hashed_password = hashed_password
    db.commit ()

    return {"message": "Password updated successfully"}
