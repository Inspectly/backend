from fastapi import APIRouter, HTTPException

from app.crud import clients
from app.schema.users import Clients

router = APIRouter()

@router.get('/')
def get_all():
    return clients.get_all()

@router.get('/{id}')
def get_one(id: int):
    return clients.get_one(id)

@router.post('/')
def create(client: Clients):
    return clients.create(client)

@router.put('/{id}')
def update(id: int, client: Clients):
    return clients.update(id, client)

@router.delete('/{id}')
def delete(id: int):
    return clients.delete(id)
