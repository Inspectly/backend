from fastapi import APIRouter, HTTPException, Body

from app.crud import issue_dispute_messages
from app.schema.properties import Issue_Dispute_Messages

router = APIRouter()

@router.get('/{issue_dispute_id}')
def get_all_by_issue_dispute_id(issue_dispute_id: int):
    return issue_dispute_messages.get_all_by_issue_dispute_id(issue_dispute_id)

@router.post('/')
def create(issue_dispute_message: Issue_Dispute_Messages, issue_dispute_id: int):
    return issue_dispute_messages.create(issue_dispute_message, issue_dispute_id)
