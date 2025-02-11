from fastapi import APIRouter, HTTPException

from app.crud import realtor_firms
from app.schema.realtor_firms import Realtor_Firms

router = APIRouter()

@router.get('/')
def get_all():
    return realtor_firms.get_all()

@router.get('/{id}')
def get_one(id: int):
    return realtor_firms.get_one(id)

@router.post('/')
def create(realtor_firm: Realtor_Firms):
    return realtor_firms.create(realtor_firm)

@router.put('/{id}')
def update(id: int, realtor_firm: Realtor_Firms):
    return realtor_firms.update(id, realtor_firm)

@router.delete('/{id}')
def delete(id: int):
    return realtor_firms.delete(id)
