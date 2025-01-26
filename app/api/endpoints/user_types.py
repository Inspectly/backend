from fastapi import APIRouter, HTTPException

from app.crud import user_types
from app.schema.user_types import User_Types

router = APIRouter()

@router.get('/')
def get_all():
    return user_types.get_all()

@router.get('/{id}')
def get_one(id: int):
    return user_types.get_one(id)

@router.post('/')
def create(user_type: User_Types):
    return user_types.create(user_type)

@router.put('/{id}')
def update(id: int, user_type: User_Types):
    return user_types.update(id, user_type)

@router.delete('/{id}')
def delete(id: int):
    return user_types.delete(id)
