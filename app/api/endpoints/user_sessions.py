import datetime
from fastapi import APIRouter, HTTPException

from app.crud import user_sessions
from app.schema.users import User_Sessions

router = APIRouter()

@router.get('/')
def get_all():
    return user_sessions.get_all()

@router.get('/{id}')
def get_one(id: int):
    return user_sessions.get_one(id)

@router.get('/user/{user_id}')
def get_user_session(user_id: str):
    return user_sessions.get_user_session(user_id)

@router.post('/')
def create(user_session: User_Sessions):
    return user_sessions.create(user_session)

@router.put('/{id}')
def update(id: int, logout_time: datetime):
    return user_sessions.update(id, logout_time)
