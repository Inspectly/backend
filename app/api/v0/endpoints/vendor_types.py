from fastapi import APIRouter, HTTPException

from app.crud import vendor_types
from app.schema.types import Vendor_Types

router = APIRouter()

@router.get('/')
def get_all():
    return vendor_types.get_all()

@router.get('/{id}')
def get_one(id: int):
    return vendor_types.get_one(id)

@router.post('/')
def create(vendor_type: Vendor_Types):
    return vendor_types.create(vendor_type)

@router.put('/{id}')
def update(id: int, vendor_type: Vendor_Types):
    return vendor_types.update(id, vendor_type)

@router.delete('/{id}')
def delete(id: int):
    return vendor_types.delete(id)
