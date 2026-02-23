from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api.runner import api_router
from app.core.config import settings

app = FastAPI(
    title = settings.PROJECT_NAME
)
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def get_all():
    return {'message': 'Go to /api/<VERSION>/ to see the API endpoints'}
app.include_router(api_router, prefix = settings.API_STR)
