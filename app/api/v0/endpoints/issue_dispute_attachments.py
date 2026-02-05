from fastapi import APIRouter, HTTPException, Body

from app.crud import issue_dispute_attachments
from app.schema.properties import Issue_Dispute_Attachments

router = APIRouter()

@router.get('/{issue_dispute_id}')
def get_all_by_issue_dispute_id(issue_dispute_id: int):
    return issue_dispute_attachments.get_all_by_issue_dispute_id(issue_dispute_id)

@router.post('/')
def create(issue_dispute_attachment: Issue_Dispute_Attachments, issue_dispute_id: int):
    return issue_dispute_attachments.create(issue_dispute_attachment, issue_dispute_id)

@router.delete('/{id}')
def delete(id: int):
    return issue_dispute_attachments.delete(id)
