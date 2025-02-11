from fastapi import HTTPException
from app.core.database import get_db_cursor
from app.schema.reports import Reports

def get_one(id: int):
    query = """
                SELECT * 
                FROM reports 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report = cursor.fetchone()
        if not report:
            raise HTTPException(status_code = 404, detail = 'Report not found')
        return dict(report)

def get_all():
    query = """
                SELECT * 
                FROM reports 
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        reports = cursor.fetchall()
        return [dict(report) for report in reports]
    
def get_user_reports(user_id: int):
    query = """
                SELECT * 
                FROM reports 
                WHERE user_id = {}
            """.format(user_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        reports = cursor.fetchall()
        return [dict(report) for report in reports]
    
def get_listing_reports(listing_id: int):
    query = """
                SELECT * 
                FROM reports 
                WHERE listing_id = {}
            """.format(listing_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        reports = cursor.fetchall()
        return [dict(report) for report in reports]
    
def create(report: Reports):
    query = """
                INSERT INTO reports 
                    (user_id, listing_id, aws_link, name)
                VALUES 
                    ({}, {}, '{}', '{}')
                RETURNING id, user_id, listing_id, created_at
            """.format(
                report.user_id, 
                report.listing_id, 
                report.aws_link, 
                report.name
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_id = cursor.fetchone()
        return dict(report_id)
    
def update(id: int, report: Reports):
    query = """
                UPDATE reports 
                SET 
                    aws_link = '{}', 
                    name = '{}' 
                WHERE id = {}
                RETURNING id, user_id, listing_id, updated_at
            """.format(
                report.aws_link, 
                report.name, 
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        report_id = cursor.fetchone()
        return dict(report_id)
    
def delete(id: int):
    query = """
                DELETE FROM reports 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Report {id} deleted successfully'}
