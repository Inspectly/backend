from fastapi import APIRouter, HTTPException

from app.crud import issue_offers
from app.schema.properties import Issue_Offers

router = APIRouter()

@router.get('/')
def get_all():
    return issue_offers.get_all()

@router.get('/{id}')
def get_one(id: int):
    return issue_offers.get_one(id)

@router.get('/issue/{issue_id}')
def get_all_by_issue_id(issue_id: int):
    return issue_offers.get_all_by_issue_id(issue_id)

@router.get('/vendor/{vendor_id}/issue/{issue_id}')
def get_all_by_vendor_id(vendor_id: int, issue_id: int):
    return issue_offers.get_all_by_vendor_id(vendor_id, issue_id)

@router.post('/')
def create(issue_offer: Issue_Offers):
    return issue_offers.create(issue_offer)

@router.put('/{id}')
def update(id: int, issue_offer: Issue_Offers):
    return issue_offers.update(id, issue_offer)

@router.delete('/{id}')
def delete(id: int):
    return issue_offers.delete(id)
