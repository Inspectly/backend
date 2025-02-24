from fastapi import APIRouter, HTTPException

from app.crud import users
from app.schema.users import Users

router = APIRouter()

@router.get('/')
def get_all():
    return users.get_all()

@router.get('/{id}')
def get_one(id: int):
    return users.get_one(id)

@router.get('/firebase/{firebase_id}')
def get_one_by_firebase_id(firebase_id: str):
    return users.get_one_by_firebase_id(firebase_id)

@router.post('/')
def create(user: Users):
    return users.create(user)

@router.put('/{id}')
def update(id: int, user: Users):
    return users.update(id, user)

@router.delete('/{id}')
def delete(id: int):
    return users.delete(id)
