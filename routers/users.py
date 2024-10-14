from http.client import HTTPException
from fastapi import Depends, HTTPException, status, Path, APIRouter
from ..models import ToDos, Users
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import  Session
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext  # To verify and create new hash


router = APIRouter(
    prefix = '/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

#Getting curr user
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


#Changing Password
@router.put("/password",status_code=status.HTTP_204_NO_CONTENT) ###
async def change_password(user: user_dependency, db:db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

# adding phone number
@router.put("/phone_number/{new_phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db:db_dependency,
                              new_phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()



