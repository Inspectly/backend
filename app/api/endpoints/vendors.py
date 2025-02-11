from fastapi import APIRouter, HTTPException

from app.crud import vendors
from app.schema.users import Vendors

router = APIRouter()

@router.get('/')
def get_all():
    return vendors.get_all()

@router.get('/{id}')
def get_one(id: int):
    return vendors.get_one(id)

@router.post('/')
def create(vendor: Vendors):
    return vendors.create(vendor)

@router.put('/{id}')
def update(id: int, vendor: Vendors):
    return vendors.update(id, vendor)

@router.delete('/{id}')
def delete(id: int):
    return vendors.delete(id)
