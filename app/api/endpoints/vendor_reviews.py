from fastapi import APIRouter, HTTPException

from app.crud import vendor_reviews
from app.schema.reviews import Vendor_Reviews

router = APIRouter()

@router.get('/')
def get_all():
    return vendor_reviews.get_all()

@router.get('/{id}')
def get_one(id: int):
    return vendor_reviews.get_one(id)

@router.get('/user_id/{user_id}')
def get_all_by_user_id(user_id: int):
    return vendor_reviews.get_all_by_user_id(user_id)

@router.get('/vendor_user_id/{vendor_user_id}')
def get_all_by_vendor_user_id(vendor_user_id: int):
    return vendor_reviews.get_all_by_vendor_user_id(vendor_user_id)

@router.post('/')
def create(vendor_review: Vendor_Reviews):
    return vendor_reviews.create(vendor_review)

@router.put('/{id}')
def update(id: int, vendor_review: Vendor_Reviews):
    return vendor_reviews.update(id, vendor_review)

@router.delete('/{id}')
def delete(id: int):
    return vendor_reviews.delete(id)
