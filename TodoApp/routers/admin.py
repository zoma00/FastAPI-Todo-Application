import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from .auth import get_current_user

from models import Todos, Users  # Ensure Users model is imported

logging.basicConfig ()
logging.getLogger ('sqlalchemy.engine').setLevel (logging.INFO)

router = APIRouter (
    prefix='/admin',
    tags=['admin']
)


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


@router.get ("/todo", status_code=status.HTTP_200_OK)
async def read_all (user: user_dependency, db: db_dependency):
    if user is None or user.get ('user_role') != 'admin':
        raise HTTPException (status_code=401, detail='Authentication Failed')
    logging.info (f"User: {user}")
    return db.query (Todos).all ()


@router.delete ("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete (user: user_dependency, db: db_dependency, todo_id: int = Path (gt=0)):
    if user is None or user.get ('user_role') != 'admin':
        raise HTTPException (status_code=401, detail='Authentication Failed')
    todo_model = db.query (Todos).filter (Todos.id == todo_id).first ()
    if todo_model is None:
        raise HTTPException (status_code=401, detail='To not found')
    db.query (Todos).filter (Todos.id == todo_id).delete ()
    db.commit()
