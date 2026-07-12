from fastapi import APIRouter, HTTPException, Body, Request

from app.crud import issue_offers
from app.schema.properties import Issue_Offers
from app.core.access import (
    get_request_user,
    require_issue_access,
    require_issue_offer_access,
    require_same_user,
)

router = APIRouter()

@router.get('/')
def get_all():
    return issue_offers.get_all()

@router.get('/{id}')
def get_one(id: int, request: Request):
    user = get_request_user(request)
    require_issue_offer_access(user, id)
    return issue_offers.get_one(id)

@router.get('/issue/{issue_id}')
def get_all_by_issue_id(issue_id: int, request: Request):
    user = get_request_user(request)
    require_issue_access(user, issue_id)
    return issue_offers.get_all_by_issue_id(issue_id)

@router.get('/vendor/{vendor_id}')
def get_all_by_vendor_id(vendor_id: int, request: Request):
    user = get_request_user(request)
    require_same_user(user, vendor_id)
    return issue_offers.get_all_by_vendor_id(vendor_id)

@router.get('/vendor/{vendor_id}/issue/{issue_id}')
def get_all_by_vendor_id_and_issue_id(vendor_id: int, issue_id: int, request: Request):
    user = get_request_user(request)
    require_same_user(user, vendor_id)
    require_issue_access(user, issue_id)
    return issue_offers.get_all_by_vendor_id_and_issue_id(vendor_id, issue_id)

@router.post('/')
def create(issue_offer: Issue_Offers, request: Request):
    user = get_request_user(request)
    if issue_offer.vendor_id is None or issue_offer.vendor_id != user['id']:
        raise HTTPException(status_code = 403, detail = 'Vendors can only create offers as themselves')
    return issue_offers.create(issue_offer)

@router.put('/{id}')
def update(id: int, issue_offer: Issue_Offers, request: Request):
    user = get_request_user(request)
    require_issue_offer_access(user, id)
    return issue_offers.update(id, issue_offer)

@router.delete('/{id}')
def delete(id: int, request: Request, issue_id: int = Body(..., embed = True)):
    user = get_request_user(request)
    require_issue_offer_access(user, id)
    return issue_offers.delete(id, issue_id)
