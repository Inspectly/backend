from fastapi import APIRouter, HTTPException

from app.crud import realtor_reviews
from app.schema.reviews import Realtor_Reviews

router = APIRouter()

@router.get('/')
def get_all():
    return realtor_reviews.get_all()

@router.get('/{id}')
def get_one(id: int):
    return realtor_reviews.get_one(id)

@router.get('/user_id/{user_id}')
def get_all_by_user_id(user_id: int):
    return realtor_reviews.get_all_by_user_id(user_id)

@router.get('/realtor_user_id/{realtor_user_id}')
def get_all_by_realtor_user_id(realtor_user_id: int):
    return realtor_reviews.get_all_by_realtor_user_id(realtor_user_id)

@router.post('/')
def create(realtor_review: Realtor_Reviews):
    return realtor_reviews.create(realtor_review)

@router.put('/{id}')
def update(id: int, realtor_review: Realtor_Reviews):
    return realtor_reviews.update(id, realtor_review)

@router.delete('/{id}')
def delete(id: int):
    return realtor_reviews.delete(id)
