import json
from fastapi import HTTPException
from app.schema.properties import Issues
from app.core.database import get_db_cursor


def _deserialize_issue(issue_dict: dict) -> dict:
    """Helper function to deserialize image_urls from JSON string to list."""
    if issue_dict.get('image_urls'):
        try:
            issue_dict['image_urls'] = json.loads(issue_dict['image_urls'])
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON or already a list, keep as is
            pass
    return issue_dict

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
        return _deserialize_issue(dict(issue))
    
def get_all():
    query = '''
                SELECT *
                FROM issues
                ORDER BY id DESC
            '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [_deserialize_issue(dict(issue)) for issue in issues]
    
def total_issues_count(vendor_assigned = False):
    query = '''
                SELECT COUNT(*) 
                FROM issues
                WHERE active = true
            '''
    if vendor_assigned:
        query += ' AND vendor_id IS NOT NULL'
    with get_db_cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()
    
def total_issues_count_filter(type = None, city = None, state = None, search = None, vendor_assigned = False):
    query = '''
        SELECT COUNT(*) 
        FROM issues i
        JOIN reports r ON i.report_id = r.id
        JOIN listings l ON r.listing_id = l.id
        WHERE 1 = 1
        AND i.active = true
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
    if vendor_assigned:
        query += ' AND i.vendor_id IS NOT NULL'
    
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def get_all_filter(limit: int = 100, offset: int = 0, type = None, city = None, state = None, search = None, vendor_assigned: bool = False):
    query = '''
        SELECT i.* 
        FROM issues i
        JOIN reports r ON i.report_id = r.id
        JOIN listings l ON r.listing_id = l.id
        WHERE 1 = 1
        AND i.active = true
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
    if vendor_assigned:
        query += ' AND i.vendor_id IS NOT NULL'
    else:
        query += ' AND i.vendor_id IS NULL'
 
    query += '''
        ORDER BY i.id DESC
        LIMIT %s OFFSET %s
    '''
    params.extend([limit, offset])
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        issues = cursor.fetchall()
        issues = [_deserialize_issue(dict(issue)) for issue in issues]
        return {
            'issues': issues,
            'total': total_issues_count(),
            'total_filtered': total_issues_count_filter(type, city, state, search, vendor_assigned)
        }
    
def get_report_issues(report_id: int):
    query = '''
                SELECT *
                FROM issues
                WHERE report_id = {}
            '''.format(report_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [_deserialize_issue(dict(issue)) for issue in issues]

def get_vendor_issues(vendor_id: int):
    query = '''
                SELECT *
                FROM issues
                WHERE vendor_id = {}
            '''.format(vendor_id)
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issues = cursor.fetchall()
        return [_deserialize_issue(dict(issue)) for issue in issues]

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
    
async def create(issue: Issues):
    # Convert image_urls list to JSON string for storage
    image_urls_json = json.dumps(issue.image_urls) if issue.image_urls else None

    query = '''
                INSERT INTO issues
                    (report_id, type, description, summary, severity, status, active, image_urls)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, report_id, vendor_id, created_at
            '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                issue.report_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.status.value,
                issue.active,
                image_urls_json
            ))
            issue = cursor.fetchone()
            return dict(issue)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))


def update(id: int, issue: Issues):
    # Convert image_urls list to JSON string for storage
    image_urls_json = json.dumps(issue.image_urls) if issue.image_urls else None

    query = '''
        UPDATE issues
        SET
            vendor_id = %s,
            type = %s,
            description = %s,
            summary = %s,
            severity = %s,
            status = %s,
            active = %s,
            image_urls = %s,
            review_status = %s
        WHERE id = %s
        RETURNING id, vendor_id, updated_at
    '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (
                issue.vendor_id,
                issue.type,
                issue.description,
                issue.summary,
                issue.severity,
                issue.status,
                issue.active,
                image_urls_json,
                issue.review_status,
                id
            ))
            updated_issue = cursor.fetchone()
            return dict(updated_issue)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
