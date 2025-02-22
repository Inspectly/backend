from fastapi import HTTPException

from app.schema.properties import Issue_Bids
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM issue_bids 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bid = cursor.fetchone()
        if not issue_bid:
            raise HTTPException(status_code = 404, detail = 'Issue bid not found')
        return dict(issue_bid)
    
def get_all():
    query = '''
                SELECT * 
                FROM issue_bids 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bids = cursor.fetchall()
        return [dict(issue_bid) for issue_bid in issue_bids]
    
def get_all_by_issue_id(issue_id: int):
    query = '''
                SELECT * 
                FROM issue_bids 
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bids = cursor.fetchall()
        return [dict(issue_bid) for issue_bid in issue_bids]
    
def get_all_by_vendor_id(vendor_id: int, issue_id: int):
    query = '''
                SELECT * 
                FROM issue_bids 
                WHERE vendor_id = {} AND issue_id = {}
            '''.format(vendor_id, issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bids = cursor.fetchall()
        return [dict(issue_bid) for issue_bid in issue_bids]
    
def create(issue_bid: Issue_Bids):
    query = '''
                INSERT INTO issue_bids 
                    (issue_id, vendor_id, price, status, comment_vendor, comment_client)
                VALUES 
                    ({}, {}, {}, '{}', '{}', '{}')
                RETURNING id, issue_id, vendor_id, created_at
            '''.format(
                issue_bid.issue_id,
                issue_bid.vendor_id,
                issue_bid.price,
                issue_bid.status,
                issue_bid.comment_vendor,
                issue_bid.comment_client
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bid_id = cursor.fetchone()
        return dict(issue_bid_id)

def update(id: int, issue_bid: Issue_Bids):
    query = '''
                UPDATE issue_bids 
                SET 
                    issue_id = {}, 
                    vendor_id = {}, 
                    price = {}, 
                    status = '{}', 
                    comment_vendor = '{}', 
                    comment_client = '{}'
                WHERE id = {}
                RETURNING id, updated_at
            '''.format(
                issue_bid.issue_id,
                issue_bid.vendor_id,
                issue_bid.price,
                issue_bid.status,
                issue_bid.comment_vendor,
                issue_bid.comment_client,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_bid_id = cursor.fetchone()
        return dict(issue_bid_id)

def delete(id: int):
    query = '''
                DELETE FROM issue_bids 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Issue bid {id} deleted successfully'}
