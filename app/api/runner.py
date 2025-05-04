from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.security import get_api_key
from app.core.database import get_db_cursor
from app.api.v0.runner_v0 import api_router as runner_v0

def require_api_key(api_key: str = Depends(get_api_key)): 
    return True

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

api_router.include_router(runner_v0, prefix = settings.V0_STR, tags = ['v0'])
