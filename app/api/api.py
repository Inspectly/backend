from fastapi import APIRouter

from app.core.database import get_db_cursor
from app.api.endpoints import users, user_types,payments, reports

api_router = APIRouter()

@api_router.get('/')
def get_all():
    return {'message': 'Welcome to the InspectlyAI API'}

@api_router.get('/status')
def get_status():
    return {'message': 'API is running'}

@api_router.get('/db_status')
def get_db_status():
    try:
        get_db_cursor()
        return {'message': 'Database is running'}
    except Exception as e:
        return {'message': 'Database is not running', 'error': str(e)} 

api_router.include_router(users.router, prefix = '/users', tags = ['users'])
api_router.include_router(user_types.router, prefix = '/user_types', tags = ['user_types'])
api_router.include_router(payments.router, prefix = '/payments', tags = ['payments'])
api_router.include_router(reports.router, prefix = '/reports', tags = ['reports'])
