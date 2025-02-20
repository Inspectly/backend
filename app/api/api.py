from fastapi import APIRouter

from app.core.database import get_db_cursor
from app.api.endpoints import (
    user_types, vendor_types, 
    users, user_logins, user_sessions, clients, realtors, vendors,
    realtor_firms,
    listings, reports, issues, issue_bids, issue_assessments, attachments, comments, notes,
    payments
)

api_router = APIRouter()

@api_router.get('/')
def get_all():
    return {'message': 'Welcome to the InspectlyAI API 😃'}

@api_router.get('/status')
def get_status():
    return {'message': 'InspectlyAI API is up and running 😃'}

@api_router.get('/db_status')
def get_db_status():
    try:
        get_db_cursor()
        return {'message': 'Database is running 😃'}
    except Exception as e:
        return {'message': 'Database is not running 😢', 'error': str(e)}

api_router.include_router(user_types.router, prefix = '/user_types', tags = ['user_types'])
api_router.include_router(vendor_types.router, prefix = '/vendor_types', tags = ['vendor_types'])

api_router.include_router(users.router, prefix = '/users', tags = ['users'])
api_router.include_router(user_logins.router, prefix = '/user_logins', tags = ['user_logins'])
api_router.include_router(user_sessions.router, prefix = '/user_sessions', tags = ['user_sessions'])
api_router.include_router(clients.router, prefix = '/clients', tags = ['clients'])
api_router.include_router(realtors.router, prefix = '/realtors', tags = ['realtors'])
api_router.include_router(vendors.router, prefix = '/vendors', tags = ['vendors'])

api_router.include_router(realtor_firms.router, prefix = '/realtor_firms', tags = ['realtor_firms'])

api_router.include_router(listings.router, prefix = '/listings', tags = ['listings'])
api_router.include_router(reports.router, prefix = '/reports', tags = ['reports'])
api_router.include_router(issues.router, prefix = '/issues', tags = ['issues'])
api_router.include_router(issue_bids.router, prefix = '/issue_bids', tags = ['issue_bids'])
api_router.include_router(issue_assessments.router, prefix = '/issue_assessments', tags = ['issue_assessments'])
api_router.include_router(attachments.router, prefix = '/attachments', tags = ['attachments'])
api_router.include_router(comments.router, prefix = '/comments', tags = ['comments'])
api_router.include_router(notes.router, prefix = '/notes', tags = ['notes'])

api_router.include_router(payments.router, prefix = '/payments', tags = ['payments'])
