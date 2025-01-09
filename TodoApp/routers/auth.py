from datetime import datetime, timedelta
from http.client import HTTPException
from fastapi import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError



router = APIRouter (
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = '43dd670d12a549ed154f79ae2e8417d25650ed7af446730ea00b544f2adc2f27'
ALGORITHM = 'HS256'
bcrypt_context = CryptContext (schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer (tokenUrl='auth/token')


class CreateUserRequest (BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token (BaseModel):
    access_token: str
    token_type: str


class PasswordReset (BaseModel):
    username: str
    new_password: str


def get_db ():
    db = SessionLocal ()
    try:
        yield db
    finally:
        db.close ()


# Dependency annotation
db_dependency = Annotated[Session, Depends (get_db)]


def authenticate_user (username: str, password: str, db):
    user = db.query (Users).filter (Users.username == username).first ()
    if not user:
        return False
    if not bcrypt_context.verify (password, user.hashed_password):
        return False
    return user


@router.post ("/", status_code=status.HTTP_201_CREATED)
async def create_user (db: db_dependency, create_user_request: CreateUserRequest):
    try:
        # Check if the username already exists
        existing_user = db.query (Users).filter (Users.username == create_user_request.username).first ()
        if existing_user:
            raise HTTPException (status_code=400, detail="Username already taken. Please choose another.")

        # Create a new user
        create_user_model = Users (
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            hashed_password=bcrypt_context.hash (create_user_request.password),
            is_active=True,
            role=create_user_request.role
        )

        db.add (create_user_model)
        db.commit ()
        return {"message": "User created successfully"}

    except Exception as e:
        logging.error (f"Error creating user: {str (e)}")
        raise HTTPException (status_code=500, detail="Internal Server Error")


@router.post ("/reset-password/")
async def reset_password (reset: PasswordReset, db: db_dependency):
    # Check if user exists
    user = db.query (Users).filter (Users.username == reset.username).first ()
    if not user:
        raise HTTPException (status_code=404, detail="User not found")

    # Hash the new password
    user.hashed_password = bcrypt_context.hash (reset.new_password)

    # Commit the changes
    db.commit ()
    db.refresh (user)

    return {"message": "Password updated successfully"}


db = SessionLocal ()
user = db.query (Users).filter (Users.username == "hello").first ()
print (user)  # Should print the user object or None
"""
test_user = Users(
    username="hello",
    email="test@example.com",
    first_name="Test",
    last_name="User",
    hashed_password=bcrypt_context.hash("test123"),
    role="user",
    is_active=True
)
db.add(test_user)
db.commit()
print("User created!")
"""
r"""
PS C:\Users\L E N O V O\fastapi\TodoApp> $body = @{
>>     username = "hello"
>>     new_password = "1234"
>> } | ConvertTo-Json -Depth 2
>>
>> $response = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/reset-password/' `
>>   -Method POST `
>>   -Headers @{ 'accept' = 'application/json'; 'Content-Type' = 'application/json' } `
>>   -Body $body
>>
>> $response
>>

message
-------
Password updated successfully

"""


def create_access_token (username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow () + expires_delta
    encode.update ({'exp': expires})
    return jwt.encode (encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user (token: Annotated[str, Depends (oauth2_bearer)]):
    try:
        payload = jwt.decode (token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get ('sub')
        user_id: int = payload.get ('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


@router.post ('/token', response_model=Token)
async def login_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends ()], db: db_dependency):
    user = authenticate_user (form_data.username, form_data.password, db)
    if not user:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user.")
    token = create_access_token (user.username, user.id, user.role, timedelta (minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


def hash_password (password: str) -> str:
    return bcrypt_context.hash (password)


r"""
Collecting passlib  for hashing pass 
  Using cached passlib-1.7.4-py2.py3-none-any.whl.metadata (1.7 kB)
Using cached passlib-1.7.4-py2.py3-none-any.whl (525 kB)
Installing collected packages: passlib
Successfully installed passlib-1.7.4

pip install bcrypt==4.0.1

## Create a token endpoint using JWT (json web token)

https://jwt.io/

(fastapienv) PS C: pip install "python-jose[cryptography]"
Collecting python-jose[cryptography]
  Using cached python_jose-3.3.0-py2.py3-none-any.whl.metadata (5.4 kB)
Collecting ecdsa!=0.15 (from python-jose[cryptography])
  Using cached ecdsa-0.19.0-py2.py3-none-any.whl.metadata (29 kB)
Collecting rsa (from python-jose[cryptography])
  Downloading rsa-4.9-py3-none-any.whl.metadata (4.2 kB)
Collecting pyasn1 (from python-jose[cryptography])
  Downloading pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
Collecting cryptography>=3.4.0 (from python-jose[cryptography])
  Downloading cryptography-44.0.0-cp39-abi3-win_amd64.whl.metadata (5.7 kB)
Collecting cffi>=1.12 (from cryptography>=3.4.0->python-jose[cryptography])
  Downloading cffi-1.17.1-cp312-cp312-win_amd64.whl.metadata (1.6 kB)
Requirement already satisfied: six>=1.9.0 in c:fastapienv\lib\site-packages (from ecdsa!=
0.15->python-jose[cryptography]) (1.17.0)
Collecting pycparser (from cffi>=1.12->cryptography>=3.4.0->python-jose[cryptography])
  Using cached pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Using cached pycparser-2.22-py3-none-any.whl (117 kB)
Installing collected packages: pycparser, pyasn1, ecdsa, rsa, cffi, python-jose, cryptography
Successfully installed cffi-1.17.1 cryptography-44.0.0 ecdsa-0.19.0 pyasn1-0.6.1 pycparser-2.22 python-jose-3.3.0 rs
a-4.9


steps:
from jose import jwt

router = APIRouter ()
SECRET_KEY = ''
(fastapienv) PS C\TodoApp> openssl rand -hex 32
43dd670d12a549ed154f79ae2e8417d25650ed7af446730ea00b544f2adc2f27
ALGORITHM = 'HS256'


"""
