from fastapi import APIRouter, HTTPException

from app.crud import payments
from app.schema.payments import Payments

router = APIRouter()

@router.get('/')
def get_all():
    return payments.get_all()

@router.get('/{id}')
def get_one(id: int):
    return payments.get_one(id)

@router.get('/user/{user_id}')
def get_user_payments(user_id: int):
    return payments.get_user_payments(user_id)

@router.post('/')
def create(payment: Payments):
    return payments.create(payment)

@router.delete('/{id}')
def delete(id: int):
    return payments.delete(id)
