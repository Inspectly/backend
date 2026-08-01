from fastapi import HTTPException

from app.core.database import get_db_cursor

from app.schema.types import Bid_Status, Offer_Update_Status
from app.schema.properties import Issue_Offer_Updates

def get_one(id: int):
    query = '''
        SELECT * 
        FROM issue_offer_updates 
        WHERE id = %s
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query, (id,))
        issue_offer_update = cursor.fetchone()
        if not issue_offer_update:
            raise HTTPException(status_code = 404, detail = 'Issue offer update not found')
        return dict(issue_offer_update)

def get_all():
    query = '''
        SELECT * 
        FROM issue_offer_updates 
        ORDER BY id DESC
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        issue_offer_updates = cursor.fetchall()
        return [dict(issue_offer_update) for issue_offer_update in issue_offer_updates]

def get_all_by_issue_id(issue_id: int):
    query = '''
        SELECT u.* 
        FROM issue_offer_updates u
        JOIN issue_offers o ON o.id = u.offer_id
        WHERE o.issue_id = %s
        ORDER BY u.id DESC
    '''
    with get_db_cursor() as cursor:
        cursor.execute(query, (issue_id,))
        issue_offer_updates = cursor.fetchall()
        return [dict(issue_offer_update) for issue_offer_update in issue_offer_updates]

def create(issue_offer_update: Issue_Offer_Updates):
    insert_query = '''
        INSERT INTO issue_offer_updates (offer_id, amount, status, reason)
        VALUES (%s, %s, %s, %s)
        RETURNING id, offer_id, created_at
    '''
    offer_query = '''
        UPDATE issue_offers
        SET status = %s
        WHERE id = %s
    '''
    try:
        with get_db_cursor() as cursor:
            # New update requests always start as pending, and the offer goes
            # into pending until the homeowner responds
            cursor.execute(insert_query, (
                issue_offer_update.offer_id,
                issue_offer_update.amount,
                Offer_Update_Status.PENDING,
                issue_offer_update.reason
            ))
            issue_offer_update_id = cursor.fetchone()
            cursor.execute(offer_query, (
                Bid_Status.PENDING,
                issue_offer_update.offer_id
            ))
            return dict(issue_offer_update_id)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))

def update(id: int, issue_offer_update: Issue_Offer_Updates):
    update_query = '''
        UPDATE issue_offer_updates
        SET
            amount = %s,
            status = %s,
            reason = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id, offer_id, amount, status, updated_at
    '''
    offer_query = '''
        UPDATE issue_offers
        SET price = %s, status = %s
        WHERE id = %s
    '''
    try:
        with get_db_cursor() as cursor:
            cursor.execute(update_query, (
                issue_offer_update.amount,
                issue_offer_update.status,
                issue_offer_update.reason,
                id
            ))
            updated = cursor.fetchone()
            if not updated:
                raise HTTPException(status_code = 404, detail = 'Issue offer update not found')
            updated = dict(updated)
            # If the homeowner accepts, the new amount becomes the offer price
            # and both tables move to accepted
            if updated['status'] == Offer_Update_Status.ACCEPTED:
                cursor.execute(offer_query, (
                    updated['amount'],
                    Bid_Status.ACCEPTED,
                    updated['offer_id']
                ))
            return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 400, detail = str(e))
