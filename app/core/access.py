from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.core.database import get_db_cursor
from app.schema.types import User_Type

def _deny(not_found: bool = True):
    # 404 avoids leaking whether a resource exists
    if not_found:
        raise HTTPException(status_code = HTTP_404_NOT_FOUND, detail = 'Not found')
    raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail = 'Forbidden')

def get_request_user(request: Request) -> dict:
    user = getattr(request.state, 'user', None)
    if not user or user.get('id') is None:
        raise HTTPException(status_code = HTTP_403_FORBIDDEN, detail = 'Authentication required')
    return user

def _issue_exists(issue_id: int) -> bool:
    with get_db_cursor() as cursor:
        cursor.execute('SELECT 1 FROM issues WHERE id = %s LIMIT 1', (issue_id,))
        return cursor.fetchone() is not None

def can_access_issue(user: dict, issue_id: int) -> bool:
    '''
    Client who owns the listing/report, vendor who bid, or assigned vendor may access.
    '''
    user_id = user.get('id')
    if user_id is None:
        return False

    query = '''
        SELECT 1
        FROM issues i
        LEFT JOIN reports r ON r.id = i.report_id
        LEFT JOIN listings l ON l.id = i.listing_id
        WHERE i.id = %s
          AND (
                r.user_id = %s
             OR l.user_id = %s
             OR i.vendor_id = %s
             OR EXISTS (
                    SELECT 1
                    FROM issue_offers o
                    WHERE o.issue_id = i.id
                      AND o.vendor_id = %s
                )
          )
        LIMIT 1
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query, (issue_id, user_id, user_id, user_id, user_id))
        return cursor.fetchone() is not None

def can_view_issue(user: dict, issue_id: int) -> bool:
    '''
    Same as can_access_issue, plus marketplace vendors may view issues to place bids.
    '''
    if can_access_issue(user, issue_id):
        return True
    if user.get('user_type') == User_Type.VENDOR.value:
        return _issue_exists(issue_id)
    return False

def can_access_issue_offer(user: dict, offer_id: int) -> bool:
    '''
    Vendor who placed the bid, or client who owns the issue, may access the offer.
    '''
    user_id = user.get('id')
    if user_id is None:
        return False

    query = '''
        SELECT 1
        FROM issue_offers o
        JOIN issues i ON i.id = o.issue_id
        LEFT JOIN reports r ON r.id = i.report_id
        LEFT JOIN listings l ON l.id = i.listing_id
        WHERE o.id = %s
          AND (
                o.vendor_id = %s
             OR r.user_id = %s
             OR l.user_id = %s
          )
        LIMIT 1
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query, (offer_id, user_id, user_id, user_id))
        return cursor.fetchone() is not None

def require_issue_access(user: dict, issue_id: int):
    if not can_access_issue(user, issue_id):
        _deny()

def require_issue_view(user: dict, issue_id: int):
    if not can_view_issue(user, issue_id):
        _deny()

def require_issue_offer_access(user: dict, offer_id: int):
    if not can_access_issue_offer(user, offer_id):
        _deny()

def require_same_user(user: dict, requested_user_id: int):
    if user.get('id') != requested_user_id:
        _deny()
