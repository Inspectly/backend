from fastapi import HTTPException

from app.core.database import get_db_cursor
from app.schema.properties import Reports

def get_one(id: int):
    query = '''
                SELECT * 
                FROM reports 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report = cursor.fetchone()
        if not report:
            raise HTTPException(status_code = 404, detail = 'Report not found')
        return dict(report)

def get_all(limit: int = 50, offset: int = 0):
    query = '''
                SELECT *
                FROM reports
                ORDER BY id DESC
                LIMIT %s OFFSET %s
            '''
    count_query = 'SELECT COUNT(*) as total FROM reports'
    with get_db_cursor() as cursor:
        cursor.execute(count_query)
        total = cursor.fetchone()['total']
        cursor.execute(query, (limit, offset))
        reports = cursor.fetchall()
        return {
            'items': [dict(report) for report in reports],
            'total': total
        }
    
def get_user_reports(user_id: int):
    query = '''
                SELECT * 
                FROM reports 
                WHERE user_id = {}
            '''.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        reports = cursor.fetchall()
        return [dict(report) for report in reports]
    
def get_listing_reports(listing_id: int):
    query = '''
                SELECT * 
                FROM reports 
                WHERE listing_id = {}
            '''.format(listing_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        reports = cursor.fetchall()
        return [dict(report) for report in reports]
    
async def create(report: Reports):
    query = '''
                INSERT INTO reports 
                    (user_id, listing_id, aws_link, name, review_status)
                VALUES 
                    ({}, {}, '{}', '{}', '{}')
                RETURNING id, user_id, listing_id, created_at
            '''.format(
                report.user_id, 
                report.listing_id, 
                report.aws_link, 
                report.name,
                report.review_status
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_id = cursor.fetchone()
            return dict(report_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, report: Reports):
    query = '''
                UPDATE reports 
                SET 
                    aws_link = '{}', 
                    name = '{}',
                    review_status = '{}'
                WHERE id = {}
                RETURNING id, user_id, listing_id, updated_at
            '''.format(
                report.aws_link, 
                report.name, 
                report.review_status,
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            report_id = cursor.fetchone()
            return dict(report_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def delete(id: int):
    query = '''
                DELETE FROM reports 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Report {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
