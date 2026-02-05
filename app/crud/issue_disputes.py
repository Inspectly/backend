from fastapi import HTTPException

from app.core.database import get_db_cursor

from app.schema.types import Dispute_Status
from app.schema.properties import Issue_Disputes

def get_one(id: int):
    query = '''
        SELECT * 
        FROM issue_disputes 
        WHERE id = {}
    '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_dispute = cursor.fetchone()
        if not issue_dispute:
            raise HTTPException(status_code = 404, detail = 'Issue dispute not found')
        return dict(issue_dispute)

def get_all():
    query = '''
        SELECT * 
        FROM issue_disputes 
        ORDER BY id DESC
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_disputes = cursor.fetchall()
        return [dict(issue_dispute) for issue_dispute in issue_disputes]

def get_all_by_issue_offer_id(issue_offer_id: int):
    query = '''
        SELECT * 
        FROM issue_disputes 
        WHERE issue_offer_id = {}
    '''.format(issue_offer_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_disputes = cursor.fetchall()
        return [dict(issue_dispute) for issue_dispute in issue_disputes]

def get_open_disputes_by_issue_offer_id(issue_offer_id: int):
    query = '''
        SELECT * 
        FROM issue_disputes 
        WHERE issue_offer_id = {} AND status = '{}'
    '''.format(issue_offer_id, Dispute_Status.OPEN)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_disputes = cursor.fetchall()
        return [dict(issue_dispute) for issue_dispute in issue_disputes]

def create(issue_dispute: Issue_Disputes):
    query = '''
        INSERT INTO issue_disputes (issue_offer_id, status, status_message)
        VALUES ({}, '{}', '{}')
        RETURNING id
    '''.format(issue_dispute.issue_offer_id, Dispute_Status.OPEN, issue_dispute.status_message)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_dispute_id = cursor.fetchone()
            return dict(issue_dispute_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, issue_dispute: Issue_Disputes):
    query = '''
        UPDATE issue_disputes 
        SET status = '{}', status_message = '{}' 
        WHERE id = {} 
        RETURNING id
    '''.format(issue_dispute.status, issue_dispute.status_message, id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_dispute_id = cursor.fetchone()
            return dict(issue_dispute_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
