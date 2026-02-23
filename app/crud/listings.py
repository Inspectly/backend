from fastapi import HTTPException

from app.schema.properties import Listings
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM listings 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        listing = cursor.fetchone()
        if not listing:
            raise HTTPException(status_code = 404, detail = 'Listing not found')
        return dict(listing)
    
def get_all(limit: int = 50, offset: int = 0):
    query = '''
                SELECT *
                FROM listings
                ORDER BY id DESC
                LIMIT %s OFFSET %s
            '''
    count_query = 'SELECT COUNT(*) as total FROM listings'
    with get_db_cursor() as cursor:
        cursor.execute(count_query)
        total = cursor.fetchone()['total']
        cursor.execute(query, (limit, offset))
        listings = cursor.fetchall()
        return {
            'items': [dict(listing) for listing in listings],
            'total': total
        }
    
def get_user_listings(user_id: int):
    query = '''
                SELECT * 
                FROM listings 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        listings = cursor.fetchall()
        return [dict(listing) for listing in listings]

def create(listing: Listings):
    query = '''
                INSERT INTO listings 
                    (user_id, address, city, state, country, postal_code, image_url)
                VALUES 
                    ({}, '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, user_id, created_at
            '''.format(
                listing.user_id,
                listing.address,
                listing.city,
                listing.state,
                listing.country,
                listing.postal_code,
                listing.image_url
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            listing = cursor.fetchone()
            return dict(listing)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, listing: Listings):
    query = '''
                UPDATE listings 
                SET 
                    address = '{}', city = '{}', state = '{}', country = '{}', postal_code = '{}', image_url = '{}'
                WHERE id = {}
                RETURNING id, user_id, updated_at
            '''.format(
                listing.address,
                listing.city,
                listing.state,
                listing.country,
                listing.postal_code,
                listing.image_url,
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            listing = cursor.fetchone()
            return dict(listing)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int):
    query = '''
                DELETE FROM listings 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Listing {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
