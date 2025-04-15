from fastapi import APIRouter, HTTPException

from app.crud import client_reviews
from app.schema.reviews import Client_Reviews

router = APIRouter()

@router.get('/')
def get_all():
    return client_reviews.get_all()

@router.get('/{id}')
def get_one(id: int):
    return client_reviews.get_one(id)

@router.get('/user_id/{user_id}')
def get_all_by_user_id(user_id: int):
    return client_reviews.get_all_by_user_id(user_id)

@router.get('/client_user_id/{client_user_id}')
def get_all_by_client_user_id(client_user_id: int):
    return client_reviews.get_all_by_client_user_id(client_user_id)

@router.post('/')
def create(client_review: Client_Reviews):
    return client_reviews.create(client_review)

@router.put('/{id}')
def update(id: int, client_review: Client_Reviews):
    return client_reviews.update(id, client_review)

@router.delete('/{id}')
def delete(id: int):
    return client_reviews.delete(id)
