from fastapi import APIRouter, HTTPException

from app.crud import user_logins
from app.schema.users import User_Logins

router = APIRouter()

@router.get('/')
def get_all():
    return user_logins.get_all()

@router.get('/{id}')
def get_one(id: int):
    return user_logins.get_one(id)

@router.get('/user/{user_id}')
def get_user_login(user_id: str):
    return user_logins.get_user_login(user_id)

@router.post('/')
def create(user_login: User_Logins):
    return user_logins.create(user_login)

@router.put('/{id}')
def update(id: int, user_login: User_Logins):
    return user_logins.update(id, user_login)

@router.delete('/{id}')
def delete(id: int):
    return user_logins.delete(id)
