from fastapi import HTTPException

from app.schema.properties import Issues
from app.core.database import get_db_cursor

def get_one(id: int):
    query = """
                SELECT * 
                FROM issues 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue = cursor.fetchone()
        if not issue:
            raise HTTPException(status_code = 404, detail = 'Issue not found')
        return dict(issue)
    
def get_all():
    query = """
                SELECT * 
                FROM issues 
                ORDER BY id DESC
            """
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]
    
def get_report_issues(report_id: int):
    query = """
                SELECT * 
                FROM issues 
                WHERE report_id = {}
            """.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]

def get_vendor_issues(vendor_id: int):
    query = """
                SELECT * 
                FROM issues 
                WHERE vendor_id = {}
            """.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]

def create(issue: Issues):
    query = """
                INSERT INTO issues 
                    (report_id, vendor_id, type, description, summary, severity, progress, cost, active)
                VALUES 
                    ({}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, report_id, vendor_id, created_at
            """.format(
                issue.report_id,
                issue.vendor_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.progress,
                issue.cost,
                issue.active
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue = cursor.fetchone()
        return dict(issue)
    
def update(id: int, issue: Issues):
    query = """
                UPDATE issues 
                SET 
                    vendor_id = {},
                    type = '{}', 
                    description = '{}', 
                    summary = '{}', 
                    severity = '{}', 
                    progress = '{}', 
                    cost = '{}', 
                    active = '{}'
                WHERE id = {}
                RETURNING id, vendor_id, updated_at
            """.format(
                issue.vendor_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.progress,
                issue.cost,
                issue.active,
                id
            )
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue = cursor.fetchone()
        return dict(issue)

def delete(id: int):
    query = """
                DELETE FROM issues 
                WHERE id = {}
            """.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return {'message': f'Issue {id} deleted successfully'}