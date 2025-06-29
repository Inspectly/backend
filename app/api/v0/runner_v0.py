from fastapi import APIRouter, Depends

from app.api.v0.endpoints import (
    issue_offers, user_types, vendor_types, 
    users, user_logins, user_sessions, clients, realtors, vendors,
    realtor_firms,
    listings, reports, issues, issue_assessments, attachments, comments, notes,
    payments, stripe_user_information, stripe_payments, stripe,
    realtor_reviews, vendor_reviews, issue_assessment_comments, client_reviews
)

api_router = APIRouter()

@api_router.get('/')
def get_all():
    return {'message': 'Welcome to the InspectlyAI API v0 😃'}

@api_router.get('/status')
def get_status():
    return {'message': 'InspectlyAI API v0 is up and running 😃'}

api_router.include_router(user_types.router, prefix = '/user_types', tags = ['user_types'])
api_router.include_router(vendor_types.router, prefix = '/vendor_types', tags = ['vendor_types'])

api_router.include_router(users.router, prefix = '/users', tags = ['users'])
api_router.include_router(user_logins.router, prefix = '/user_logins', tags = ['user_logins'])
api_router.include_router(user_sessions.router, prefix = '/user_sessions', tags = ['user_sessions'])

api_router.include_router(clients.router, prefix = '/clients', tags = ['clients'])
api_router.include_router(realtors.router, prefix = '/realtors', tags = ['realtors'])
api_router.include_router(vendors.router, prefix = '/vendors', tags = ['vendors'])

api_router.include_router(client_reviews.router, prefix = '/client_reviews', tags = ['client_reviews'])
api_router.include_router(realtor_reviews.router, prefix = '/realtor_reviews', tags = ['realtor_reviews'])
api_router.include_router(vendor_reviews.router, prefix = '/vendor_reviews', tags = ['vendor_reviews'])

api_router.include_router(realtor_firms.router, prefix = '/realtor_firms', tags = ['realtor_firms'])

api_router.include_router(listings.router, prefix = '/listings', tags = ['listings'])
api_router.include_router(reports.router, prefix = '/reports', tags = ['reports'])
api_router.include_router(issues.router, prefix = '/issues', tags = ['issues'])

api_router.include_router(issue_offers.router, prefix = '/issue_offers', tags = ['issue_offers'])
api_router.include_router(issue_assessments.router, prefix = '/issue_assessments', tags = ['issue_assessments'])
api_router.include_router(issue_assessment_comments.router, prefix = '/issue_assessment_comments', tags = ['issue_assessment_comments'])

api_router.include_router(attachments.router, prefix = '/attachments', tags = ['attachments'])
api_router.include_router(comments.router, prefix = '/comments', tags = ['comments'])
api_router.include_router(notes.router, prefix = '/notes', tags = ['notes'])

api_router.include_router(payments.router, prefix = '/payments', tags = ['payments'])
api_router.include_router(stripe_user_information.router, prefix = '/stripe_user_information', tags = ['stripe_user_information'])
api_router.include_router(stripe_payments.router, prefix = '/stripe_payments', tags = ['stripe_payments'])

api_router.include_router(stripe.router, prefix="/stripe", tags=["stripe"])
