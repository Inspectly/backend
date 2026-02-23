from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.api import resolve_params

from app.crud import listings
from app.schema.properties import Listings

router = APIRouter()

@router.get('/', response_model=Page)
def get_all():
    params = resolve_params()
    raw = params.to_raw_params()
    result = listings.get_all(limit=raw.limit, offset=raw.offset)
    return Page.create(
        items=result['items'],
        params=params,
        total=result['total'],
    )

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
