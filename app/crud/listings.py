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
    
def get_all():
    query = '''
                SELECT * 
                FROM listings
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        listings = cursor.fetchall()
        return [dict(listing) for listing in listings]
    
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
    with get_db_cursor() as cursor:
        cursor.execute(query)
        listing = cursor.fetchone()
        return dict(listing)
    
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
    with get_db_cursor() as cursor:
        cursor.execute(query)
        listing = cursor.fetchone()
        return dict(listing)
    
def delete(id: int):
    query = '''
                DELETE FROM listings 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Listing {id} deleted successfully'}