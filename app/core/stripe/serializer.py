from app.crud.issue_offers import (
    get_one as get_issue_offer_by_id
)
from app.crud.issues import (
    get_one as get_issue_by_id
)
from app.crud.reports import (
    get_one as get_report_by_id
)
from app.crud import stripe_user_information

def validate_user(user_id: int):
    try:
        user_stripe_information = stripe_user_information.get_user_stripe_information(user_id)
        if not user_stripe_information:
            raise LookupError(f'User with id {user_id} does not have a stripe account')
        return {
            'user_id': user_id,
            'stripe_user_id': user_stripe_information['stripe_user_id']
        }
    except LookupError:
        raise
    except Exception as e:
        raise Exception(f'Internal server error: {e}')

def validate_issue_offer(offer_id: int):
    try:
        offer = get_issue_offer_by_id(offer_id)
        if not offer:
            raise LookupError(f'Offer with id {offer_id} not found')
        if (offer['status'] in ['accepted', 'rejected']):
            raise ValueError(f'Offer with id {offer_id} is already {offer["status"]}')
        
        issue = get_issue_by_id(offer['issue_id'])
        if not issue:
            raise LookupError(f'Issue with id {offer["issue_id"]} not found')
        
        report = get_report_by_id(issue['report_id'])
        if not report:
            raise LookupError(f'Report with id {issue["report_id"]} not found')
        
        return offer
    except (LookupError, ValueError):
        raise
    except Exception as e:
        raise RuntimeError(f'Internal server error: {e}')

def validate_webhook_metadata(session):
    offer_id = session['metadata'].get('offer_id')
    client_id = session['metadata'].get('client_id')
    vendor_id = session['metadata'].get('vendor_id')
    
    if not offer_id:
        raise ValueError('Webhook missing offer_id in metadata')
    if not client_id:
        raise ValueError('Webhook missing client_id in metadata')
    if not vendor_id:
        raise ValueError('Webhook missing vendor_id in metadata')
    
    offer = get_issue_offer_by_id(int(offer_id))
    if not offer:
        raise ValueError('Offer not found')
    
    issue_id = offer['issue_id']
    
    if str(vendor_id) != str(offer['vendor_id']):
        raise ValueError('Vendor ID mismatch')
    
    issue = get_issue_by_id(issue_id)
    if not issue:
        raise ValueError('Issue not found')
    
    return offer_id, client_id, vendor_id, offer, issue, issue_id
