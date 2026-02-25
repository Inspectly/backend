from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Issue_Dispute_Attachments

def get_all_by_issue_dispute_id(issue_dispute_id: int):
    query = '''
        SELECT * 
        FROM issue_dispute_attachments 
        WHERE issue_dispute_id = {}
        ORDER BY created_at DESC
    '''.format(issue_dispute_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_dispute_attachments = cursor.fetchall()
        return [dict(issue_dispute_attachment) for issue_dispute_attachment in issue_dispute_attachments]

def create(issue_dispute_attachment: Issue_Dispute_Attachments, issue_dispute_id: int):
    query = '''
        INSERT INTO issue_dispute_attachments (issue_dispute_id, attachment_url, user_type)
        VALUES ({}, '{}', '{}')
        RETURNING id
    '''.format(issue_dispute_id, issue_dispute_attachment.attachment_url, issue_dispute_attachment.user_type.value)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_dispute_attachment_id = cursor.fetchone()
            return dict(issue_dispute_attachment_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    query = '''
        DELETE FROM issue_dispute_attachments 
        WHERE id = {}
        RETURNING id
    '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_dispute_attachment_id = cursor.fetchone()
        return dict(issue_dispute_attachment_id)
