from app.core.stripe.types import Validation_Response
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
