from sqlalchemy.orm import Session
from models import Users  # Import your User model


def create_user (db: Session, email: str, username: str, first_name: str, last_name: str, hashed_password: str):
    # Check if the username or email already exists
    if db.query (Users).filter ((Users.username == username) | (Users.email == email)).first ():
        raise ValueError ("Username or email already exists")

    new_user = Users (
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hashed_password,
        is_active=True,
        role='user'
    )

    db.add (new_user)
    db.commit ()
    