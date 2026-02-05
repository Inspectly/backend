from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Issue_Dispute_Messages

def get_all_by_issue_dispute_id(issue_dispute_id: int):
    query = '''
        SELECT * 
        FROM issue_dispute_messages 
        WHERE issue_dispute_id = {}
        ORDER BY created_at DESC
    '''.format(issue_dispute_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_dispute_messages = cursor.fetchall()
        return [dict(issue_dispute_message) for issue_dispute_message in issue_dispute_messages]

def create(issue_dispute_message: Issue_Dispute_Messages, issue_dispute_id: int):
    query = '''
        INSERT INTO issue_dispute_messages (issue_dispute_id, message, user_type)
        VALUES ({}, '{}', '{}')
        RETURNING id
    '''.format(issue_dispute_id, issue_dispute_message.message, issue_dispute_message.user_type)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_dispute_message_id = cursor.fetchone()
            return dict(issue_dispute_message_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
