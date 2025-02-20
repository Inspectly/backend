from fastapi import APIRouter, HTTPException

from app.crud import issue_bids
from app.schema.properties import Issue_Bids

router = APIRouter()

@router.get('/')
def get_all():
    return issue_bids.get_all()

@router.get('/{id}')
def get_one(id: int):
    return issue_bids.get_one(id)

@router.get('/issue/{issue_id}')
def get_all_by_issue_id(issue_id: int):
    return issue_bids.get_all_by_issue_id(issue_id)

@router.get('/vendor/{vendor_id}/issue/{issue_id}')
def get_all_by_vendor_id(vendor_id: int, issue_id: int):
    return issue_bids.get_all_by_vendor_id(vendor_id, issue_id)

@router.post('/')
def create(issue_bid: Issue_Bids):
    return issue_bids.create(issue_bid)

@router.put('/{id}')
def update(id: int, issue_bid: Issue_Bids):
    return issue_bids.update(id, issue_bid)

@router.delete('/{id}')
def delete(id: int):
    return issue_bids.delete(id)
