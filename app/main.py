from fastapi import FastAPI

from app.api.runner import api_router
from app.core.config import settings

app = FastAPI(
    title = settings.PROJECT_NAME
)
@app.get('/')
def get_all():
    return {'message': 'Go to /api/<VERSION>/ to see the API endpoints'}
app.include_router(api_router, prefix = settings.API_STR)
