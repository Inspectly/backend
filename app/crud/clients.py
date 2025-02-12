from fastapi import HTTPException

from app.schema.users import Clients
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM clients 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client = cursor.fetchone()
        if not client:
            raise HTTPException(status_code = 404, detail = 'Client not found')
        return dict(client)

def get_all():
    query = '''
                SELECT * 
                FROM clients 
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        clients = cursor.fetchall()
        return [dict(client) for client in clients]
    
def create(client: Clients):
    query = '''
                INSERT INTO clients 
                    (user_id, first_name, last_name, email, phone, address, city, state, country, postal_code)
                VALUES 
                    ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, user_id, first_name, created_at
            '''.format(
                client.user_id,
                client.first_name,
                client.last_name,
                client.email,
                client.phone,
                client.address,
                client.city,
                client.state,
                client.country,
                client.postal_code
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client = cursor.fetchone()
        return dict(client)

def update(id: int, client: Clients):
    query = '''
                UPDATE clients 
                SET 
                    user_id = '{}', 
                    first_name = '{}', 
                    last_name = '{}', 
                    email = '{}', 
                    phone = '{}', 
                    address = '{}', 
                    city = '{}', 
                    state = '{}', 
                    country = '{}', 
                    postal_code = '{}'
                WHERE id = {}
                RETURNING id, user_id, first_name, updated_at
            '''.format(
                client.user_id, 
                client.first_name, 
                client.last_name, 
                client.email, 
                client.phone, 
                client.address, 
                client.city, 
                client.state, 
                client.country, 
                client.postal_code, 
                id
            ) 
    with get_db_cursor() as cursor:
        cursor.execute(query)
        client = cursor.fetchone()
        return dict(client)
    
def delete(id: int):
    query = '''
                DELETE FROM clients 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Client {id} deleted successfully'}
