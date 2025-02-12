from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Attachments

def get_one(id: int):
    query = '''
                SELECT * 
                FROM attachments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachment = cursor.fetchone()
        if not attachment:
            raise HTTPException(status_code = 404, detail = 'Attachment not found')
        return dict(attachment)
    
def get_all():
    query = '''
                SELECT * 
                FROM attachments 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachments = cursor.fetchall()
        return [dict(attachment) for attachment in attachments]

def get_issue_attachments(issue_id: int):
    query = '''
                SELECT * 
                FROM attachments 
                WHERE issue_id = {}
            '''.format(issue_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachments = cursor.fetchall()
        return [dict(attachment) for attachment in attachments]

def get_user_attachments(user_id: int):
    query = '''
                SELECT * 
                FROM attachments 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachments = cursor.fetchall()
        return [dict(attachment) for attachment in attachments]
    
def create(attachment: Attachments):
    query = '''
                INSERT INTO attachments 
                    (issue_id, user_id, name, type, url)
                VALUES 
                    ({}, {}, '{}', '{}', '{}')
                RETURNING id, issue_id, user_id, created_at
            '''.format(
                attachment.issue_id,
                attachment.user_id,
                attachment.name,
                attachment.attachment_type,
                attachment.url
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachment = cursor.fetchone()
        return dict(attachment)

def update(id: int, attachment: Attachments):
    query = '''
                UPDATE attachments 
                SET 
                    name = '{}', 
                    type = '{}', 
                    url = '{}'
                WHERE id = {}
                RETURNING id, issue_id, user_id, updated_at
            '''.format(
                attachment.name,
                attachment.type,
                attachment.url,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        attachment = cursor.fetchone()
        return dict(attachment)

def delete(id: int):
    query = '''
                DELETE FROM attachments 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Attachment {id} deleted successfully'}
