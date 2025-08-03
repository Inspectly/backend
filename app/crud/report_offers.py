from fastapi import HTTPException

from app.schema.types import User_Type
from app.core.database import get_db_cursor
from app.schema.properties import Report_Offers

from app.utils.helpers import get_user_type_from_id

def get_one(id: int):
    query = '''
                SELECT * 
                FROM report_offers 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_offer = cursor.fetchone()
        if not report_offer:
            raise HTTPException(status_code = 404, detail = 'Report offer not found')
        return dict(report_offer)
    
def get_all():
    query = '''
                SELECT * 
                FROM report_offers 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_offers = cursor.fetchall()
        return [dict(report_offer) for report_offer in report_offers]
    
def get_all_by_report_id(report_id: int):
    query = '''
                SELECT * 
                FROM report_offers 
                WHERE report_id = {}
            '''.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_offers = cursor.fetchall()
        return [dict(report_offer) for report_offer in report_offers]
    
def get_all_by_vendor_id(vendor_id: int):
    query = '''
                SELECT * 
                FROM report_offers 
                WHERE vendor_id = {}
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_offers = cursor.fetchall()
        return [dict(report_offer) for report_offer in report_offers]

def get_all_by_vendor_id_and_report_id(vendor_id: int, report_id: int):
    query = '''
                SELECT * 
                FROM report_offers 
                WHERE vendor_id = {} AND report_id = {}
            '''.format(vendor_id, report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_offers = cursor.fetchall()
        return [dict(report_offer) for report_offer in report_offers]
    
    
def create(report_offer: Report_Offers):
    user_type = get_user_type_from_id(report_offer.vendor_id)
    if (user_type != User_Type.VENDOR):
        raise HTTPException(status_code = 400, detail = 'Offer is not from a vendor')
    query = '''
                INSERT INTO report_offers 
                    (report_id, vendor_id, price, status, comment_vendor, comment_client)
                VALUES 
                    ({}, {}, {}, '{}', '{}', '{}')
                RETURNING id, report_id, vendor_id, created_at
            '''.format(
                report_offer.report_id,
                report_offer.vendor_id,
                report_offer.price,
                report_offer.status,
                report_offer.comment_vendor,
                report_offer.comment_client
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_offer_id = cursor.fetchone()
            return dict(report_offer_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, report_offer: Report_Offers):
    query = '''
                UPDATE report_offers 
                SET 
                    price = {}, 
                    status = '{}', 
                    comment_vendor = '{}', 
                    comment_client = '{}',
                    user_last_viewed = '{}'
                WHERE id = {}
                AND report_id = {}
                RETURNING id, updated_at
            '''.format(
                report_offer.price,
                report_offer.status,
                report_offer.comment_vendor,
                report_offer.comment_client,
                report_offer.user_last_viewed,
                id,
                report_offer.report_id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_offer_id = cursor.fetchone()
            return dict(report_offer_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int, report_id: int):
    query = '''
                DELETE FROM report_offers 
                WHERE id = {}
                AND report_id = {}
            '''.format(id, report_id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Report offer {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
