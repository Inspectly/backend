from fastapi import APIRouter, HTTPException

from app.crud import stripe_user_information
from app.schema.payments import User_Stripe_Information

router = APIRouter()

@router.get('/')
def get_all():
    return stripe_user_information.get_all()

@router.get('/{id}')
def get_one(id: int):
    return stripe_user_information.get_one(id)

@router.get('/user/{user_id}')
def get_user_stripe_information(user_id: int):
    return stripe_user_information.get_user_stripe_information(user_id)

@router.get('/stripe_user_id/{stripe_user_id}')
def get_user_stripe_information_by_stripe_user_id(stripe_user_id: str):
    return stripe_user_information.get_user_stripe_information_by_stripe_user_id(stripe_user_id)

@router.post('/')
def create(user_stripe_information: User_Stripe_Information):
    return stripe_user_information.create(user_stripe_information)

@router.put('/{id}')
def update(id: int, user_stripe_information: User_Stripe_Information):
    return stripe_user_information.update(id, user_stripe_information)

@router.delete('/{id}')
def delete(id: int):
    return stripe_user_information.delete(id)
