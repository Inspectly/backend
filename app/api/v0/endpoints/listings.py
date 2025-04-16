from fastapi import APIRouter, HTTPException

from app.crud import listings
from app.schema.properties import Listings

router = APIRouter()

@router.get('/')
def get_all():
    return listings.get_all()

@router.get('/{id}')
def get_one(id: int):
    return listings.get_one(id)

@router.get('/user/{user_id}')
def get_user_listings(user_id: int):
    return listings.get_user_listings(user_id)

@router.post('/')
def create(listing: Listings):
    return listings.create(listing)

@router.put('/{id}')
def update(id: int, listing: Listings):
    return listings.update(id, listing)

@router.delete('/{id}')
def delete(id: int):
    return listings.delete(id)
