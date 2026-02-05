'''
1. get all disputes for an issue_offer done
2. get dispute by id + all messages and attachments
3. create a dispute done
4. update a dispute done
5. add a message to a dispute done
6. add an attachment to a dispute done
7. delete an attachment from a dispute done

#dashboard
8. get all disputes
9. get all disputes for the user and vendor
10. get all disputes for each status
'''

from fastapi import APIRouter, HTTPException, Body

from app.crud import issue_disputes, issue_dispute_messages, issue_dispute_attachments
from app.schema.properties import Issue_Disputes

router = APIRouter()

@router.get('/{id}')
def get_one(id: int):
    return issue_disputes.get_one(id)

@router.get('/')
def get_all():
    return issue_disputes.get_all()

@router.get('/issue_offer/{issue_offer_id}')
def get_all_by_issue_offer_id(issue_offer_id: int):
    return issue_disputes.get_all_by_issue_offer_id(issue_offer_id)

@router.get('/issue_offer/{issue_offer_id}/open')
def get_open_disputes_by_issue_offer_id(issue_offer_id: int):
    return issue_disputes.get_open_disputes_by_issue_offer_id(issue_offer_id)

# add a router, that will get a issue_offer_id, and will rertieve the status of the issue dispute, the status message, and a list containing all the messages and all the attachments.
# each message will contain a user_type, the message and created_at time.
# each attachment will contain the user_type, the attachment_url and created_at time.
# everything in that list should be sorted by created_at time, from oldest to newest.

@router.get('/issue_offer/{issue_offer_id}/details')
def get_dispute_details_by_issue_offer_id(issue_offer_id: int):
    disputes = issue_disputes.get_all_by_issue_offer_id(issue_offer_id)
    if not disputes:
        raise HTTPException(status_code=404, detail='No dispute found for this issue offer')

    dispute = disputes[0]
    dispute_id = dispute['id']

    messages = issue_dispute_messages.get_all_by_issue_dispute_id(dispute_id)
    attachments = issue_dispute_attachments.get_all_by_issue_dispute_id(dispute_id)

    message_items = [
        {'type': 'message', 'user_type': m['user_type'], 'message': m['message'], 'created_at': m['created_at']}
        for m in messages
    ]
    attachment_items = [
        {'type': 'attachment', 'user_type': a['user_type'], 'attachment_url': a['attachment_url'], 'created_at': a['created_at']}
        for a in attachments
    ]

    combined = message_items + attachment_items
    combined.sort(key=lambda x: x['created_at'])

    return {
        'status': dispute['status'],
        'status_message': dispute['status_message'],
        'items': combined
    }

@router.post('/')
def create(issue_dispute: Issue_Disputes):
    return issue_disputes.create(issue_dispute)

@router.put('/{id}')
def update(id: int, issue_dispute: Issue_Disputes):
    return issue_disputes.update(id, issue_dispute)
