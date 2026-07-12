import json
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Header, HTTPException, Request, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

load_dotenv(override = True)

api_key_header = APIKeyHeader(name = 'InspectlyAI-API-Key', auto_error = False)

_firebase_app = None

# Paths under /api/v0 that do not require a logged-in user (prefix match)
AUTH_EXEMPT_PREFIXES = (
    '/stripe/checkout/webhook',
    '/status',
    '/user_types',
    '/tasks',
)

def _init_firebase():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    import firebase_admin
    from firebase_admin import credentials

    if firebase_admin._apps:
        _firebase_app = firebase_admin.get_app()
        return _firebase_app

    creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
    project_id = os.getenv('FIREBASE_PROJECT_ID')

    if not creds_json:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Firebase is not configured on the server'
        )

    try:
        creds_payload = json.loads(creds_json.strip().strip("'").strip('"'))
        cred = credentials.Certificate(creds_payload)
    except Exception:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Invalid FIREBASE_CREDENTIALS_JSON'
        )

    options = {'projectId': project_id} if project_id else None
    _firebase_app = firebase_admin.initialize_app(cred, options)
    return _firebase_app

def _v0_relative_path(path: str) -> str:
    marker = '/v0'
    if marker in path:
        relative = path.split(marker, 1)[1]
        return relative if relative else '/'
    return path

def _is_auth_exempt(request: Request) -> bool:
    path = request.url.path.rstrip('/')
    if path.endswith('/v0') or path.endswith('/api'):
        return True
    relative = _v0_relative_path(path)
    return any(
        relative == prefix or relative.startswith(prefix + '/')
        for prefix in AUTH_EXEMPT_PREFIXES
    )

def _is_user_registration(request: Request) -> bool:
    path = request.url.path.rstrip('/')
    return request.method == 'POST' and path.endswith('/users')

def _extract_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Missing Authorization header'
        )
    parts = authorization.split(' ', 1)
    if len(parts) != 2 or parts[0].lower() != 'bearer' or not parts[1].strip():
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Authorization header. Expected: Bearer <token>'
        )
    return parts[1].strip()

def _verify_firebase_token(token: str) -> dict:
    _init_firebase()
    from firebase_admin import auth as firebase_auth
    try:
        return firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Invalid or expired authentication token'
        )

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if (api_key_header == os.getenv('InspectlyAI-API-Key')):
        return api_key_header
    else:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN, detail = 'Could not validate API key'
        )

async def authenticate_user(
    request: Request,
    authorization: Optional[str] = Header(default = None)
):
    '''
    Verify Firebase ID token and attach the DB user to request.state.user.
    Exempt: health/status, stripe webhook.
    User registration (POST /users): token required, DB user may not exist yet.
    '''
    if _is_auth_exempt(request):
        request.state.user = None
        return None

    token = _extract_bearer_token(authorization)
    decoded = _verify_firebase_token(token)
    firebase_id = decoded.get('uid')
    if not firebase_id:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'Invalid authentication token'
        )

    if _is_user_registration(request):
        user = {'id': None, 'firebase_id': firebase_id, 'user_type': None}
        request.state.user = user
        return user

    from app.crud import users
    try:
        user = users.get_one_by_firebase_id(firebase_id)
    except HTTPException:
        raise HTTPException(
            status_code = HTTP_401_UNAUTHORIZED,
            detail = 'User is not registered'
        )

    request.state.user = user
    return user
