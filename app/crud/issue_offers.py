import os
from fastapi import HTTPException
import logfire

from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.schema.properties import Issue_Offers

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM issue_offers 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offer = cursor.fetchone()
        if not issue_offer:
            raise HTTPException(status_code = 404, detail = 'Issue offer not found')
        return dict(issue_offer)
    
def get_all():
    query = '''
                SELECT * 
                FROM issue_offers 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offers = cursor.fetchall()
        return [dict(issue_offer) for issue_offer in issue_offers]
    
def get_all_by_issue_id(issue_id: int):
    query = '''
                SELECT * 
                FROM issue_offers 
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offers = cursor.fetchall()
        return [dict(issue_offer) for issue_offer in issue_offers]
    
def get_all_by_vendor_id(vendor_id: int):
    query = '''
                SELECT * 
                FROM issue_offers 
                WHERE vendor_id = {}
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offers = cursor.fetchall()
        return [dict(issue_offer) for issue_offer in issue_offers]

def get_all_by_vendor_id_and_issue_id(vendor_id: int, issue_id: int):
    query = '''
                SELECT * 
                FROM issue_offers 
                WHERE vendor_id = {} AND issue_id = {}
            '''.format(vendor_id, issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offers = cursor.fetchall()
        return [dict(issue_offer) for issue_offer in issue_offers]
    
    
def create(issue_offer: Issue_Offers):
    user_type = get_user_type_from_id(issue_offer.vendor_id)
    if (user_type != User_Type.VENDOR):
        raise HTTPException(status_code = 400, detail = 'Offer is not from a vendor')
    query = '''
                INSERT INTO issue_offers 
                    (issue_id, vendor_id, price, status, comment_vendor, comment_client)
                VALUES 
                    ({}, {}, {}, '{}', '{}', '{}')
                RETURNING id, issue_id, vendor_id, created_at
            '''.format(
                issue_offer.issue_id,
                issue_offer.vendor_id,
                issue_offer.price,
                issue_offer.status,
                issue_offer.comment_vendor,
                issue_offer.comment_client
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_offer_id = cursor.fetchone()
            return dict(issue_offer_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, issue_offer: Issue_Offers):
    query = '''
                UPDATE issue_offers 
                SET 
                    price = {}, 
                    status = '{}', 
                    comment_vendor = '{}', 
                    comment_client = '{}',
                    user_last_viewed = '{}'
                WHERE id = {}
                AND issue_id = {}
                RETURNING id, updated_at
            '''.format(
                issue_offer.price,
                issue_offer.status,
                issue_offer.comment_vendor,
                issue_offer.comment_client,
                issue_offer.user_last_viewed,
                id,
                issue_offer.issue_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue_offer_id = cursor.fetchone()
            return dict(issue_offer_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, issue_id: int):
    query = '''
                DELETE FROM issue_offers 
                WHERE id = {}
                AND issue_id = {}
            '''.format(id, issue_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Issue offer {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
