from fastapi import APIRouter, HTTPException, Request

from app.crud import issue_offers, issue_offer_updates
from app.schema.properties import Issue_Offer_Updates
from app.schema.types import Offer_Update_Status
from app.core.access import (
    get_request_user,
    is_admin,
    require_issue_access,
    require_issue_offer_access,
)

router = APIRouter()

@router.get('/')
def get_all():
    return issue_offer_updates.get_all()

@router.get('/{id}')
def get_one(id: int, request: Request):
    user = get_request_user(request)
    issue_offer_update = issue_offer_updates.get_one(id)
    require_issue_offer_access(user, issue_offer_update['offer_id'])
    return issue_offer_update

@router.get('/issue/{issue_id}')
def get_all_by_issue_id(issue_id: int, request: Request):
    user = get_request_user(request)
    require_issue_access(user, issue_id)
    return issue_offer_updates.get_all_by_issue_id(issue_id)

@router.post('/')
def create(issue_offer_update: Issue_Offer_Updates, request: Request):
    user = get_request_user(request)
    offer = issue_offers.get_one(issue_offer_update.offer_id)
    if not is_admin(user) and offer['vendor_id'] != user['id']:
        raise HTTPException(status_code = 403, detail = 'Vendors can only request updates on their own offers')
    return issue_offer_updates.create(issue_offer_update)

@router.put('/{id}')
def update(id: int, issue_offer_update: Issue_Offer_Updates, request: Request):
    user = get_request_user(request)
    existing = issue_offer_updates.get_one(id)
    require_issue_offer_access(user, existing['offer_id'])
    if not is_admin(user):
        offer = issue_offers.get_one(existing['offer_id'])
        is_offer_vendor = offer['vendor_id'] == user['id']
        if issue_offer_update.status in (Offer_Update_Status.ACCEPTED, Offer_Update_Status.REJECTED) and is_offer_vendor:
            raise HTTPException(status_code = 403, detail = 'Only the homeowner can accept or reject an offer update')
        if issue_offer_update.status == Offer_Update_Status.WITHDRAWN and not is_offer_vendor:
            raise HTTPException(status_code = 403, detail = 'Only the vendor can withdraw an offer update')
    return issue_offer_updates.update(id, issue_offer_update)
