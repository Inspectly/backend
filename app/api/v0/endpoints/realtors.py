from fastapi import APIRouter, HTTPException

from app.crud import realtors
from app.schema.users import Realtors

router = APIRouter()

@router.get('/')
def get_all():
    return realtors.get_all()

@router.get('/{id}')
def get_one(id: int):
    return realtors.get_one(id)

@router.post('/')
def create(realtor: Realtors):
    return realtors.create(realtor)

@router.put('/{id}')
def update(id: int, realtor: Realtors):
    return realtors.update(id, realtor)

@router.delete('/{id}')
def delete(id: int):
    return realtors.delete(id)
