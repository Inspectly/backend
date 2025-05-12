from fastapi import HTTPException

from app.schema.properties import Issues
from app.core.database import get_db_cursor

def get_one(id: int):
    query = '''
                SELECT * 
                FROM issues 
                WHERE id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue = cursor.fetchone()
        if not issue:
            raise HTTPException(status_code = 404, detail = 'Issue not found')
        return dict(issue)
    
def get_all():
    query = '''
                SELECT * 
                FROM issues 
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]
    
def get_all_paginated(limit: int = 100, offset: int = 0, type = None, city = None, state = None, search = None):
    query = '''
        SELECT i.* 
        FROM issues i
        JOIN reports r ON i.report_id = r.id
        JOIN listings l ON r.listing_id = l.id
        WHERE 1=1
    '''
    params = []
    if type:
        query += ' AND i.type = %s'
        params.append(type)
    if city:
        query += ' AND l.city = %s'
        params.append(city)
    if state:
        query += ' AND l.state = %s'
        params.append(state)
    if search:
        query += ' AND i.summary ILIKE %s'
        params.append(f'%{search}%')
 
    query += '''
        ORDER BY i.id DESC
        LIMIT %s OFFSET %s
    '''
    params.extend([limit, offset])
    
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        issues = cursor.fetchall()
        issues = [dict(issue) for issue in issues]
        return {'issues': issues, 'total': len(issues)}
    
def get_report_issues(report_id: int):
    query = '''
                SELECT * 
                FROM issues 
                WHERE report_id = {}
            '''.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]

def get_vendor_issues(vendor_id: int):
    query = '''
                SELECT * 
                FROM issues 
                WHERE vendor_id = {}
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [dict(issue) for issue in issues]

def get_all_issue_addresses():
    query = '''
                SELECT 
                    i.id as issue_id,
                    l.address,
                    l.city,
                    l.state,
                    l.country,
                    l.postal_code
                FROM 
                    issues i
                JOIN 
                    reports r ON i.report_id = r.id
                JOIN 
                    listings l ON r.listing_id = l.id
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        addresses = cursor.fetchall()
        return [dict(address) for address in addresses]

def get_all_issue_addresses_issue_ids(issue_ids: list[int]):
    query = '''
                SELECT 
                    i.id as issue_id,
                    l.address,
                    l.city,
                    l.state,
                    l.country,
                    l.postal_code
                FROM 
                    issues i
                JOIN 
                    reports r ON i.report_id = r.id
                JOIN 
                    listings l ON r.listing_id = l.id
                WHERE 
                    i.id IN ({})
            '''.format(', '.join(str(id) for id in issue_ids))
    with get_db_cursor() as cursor:
        cursor.execute(query)
        addresses = cursor.fetchall()
        return [dict(address) for address in addresses]

def get_issue_address(id: int):
    query = '''
                SELECT 
                    l.address,
                    l.city,
                    l.state,
                    l.country,
                    l.postal_code
                FROM 
                    issues i
                JOIN 
                    reports r ON i.report_id = r.id
                JOIN 
                    listings l ON r.listing_id = l.id
                WHERE 
                    i.id = {}
            '''.format(id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        address = cursor.fetchone()
        if not address:
            raise HTTPException(status_code = 404, detail = 'Address not found')
        return dict(address)
    
def create(issue: Issues):
    query = '''
                INSERT INTO issues 
                    (report_id, type, description, summary, severity, status, active, image_url)
                VALUES 
                    ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING id, report_id, vendor_id, created_at
            '''.format(
                issue.report_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.status,
                issue.active,
                issue.image_url
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue = cursor.fetchone()
            return dict(issue)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
    
def update(id: int, issue: Issues):
    query = '''
                UPDATE issues 
                SET 
                    vendor_id = {},
                    type = '{}', 
                    description = '{}', 
                    summary = '{}', 
                    severity = '{}', 
                    status = '{}', 
                    active = '{}',
                    image_url = '{}'
                WHERE id = {}
                RETURNING id, vendor_id, updated_at
            '''.format(
                issue.vendor_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.status,
                issue.active,
                issue.image_url,
                id
            )
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            issue = cursor.fetchone()
            return dict(issue)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def delete(id: int):
    query = '''
                DELETE FROM issues 
                WHERE id = {}
            '''.format(id)
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return {'message': f'Issue {id} deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
