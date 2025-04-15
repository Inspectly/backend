import os
from dotenv import load_dotenv

from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

load_dotenv(override = True)

api_key_header = APIKeyHeader(name = 'InspectlyAI-API-Key', auto_error = False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if (api_key_header == os.getenv('InspectlyAI-API-Key')):
        return api_key_header
    else:
        raise HTTPException(
            status_code = HTTP_403_FORBIDDEN, detail = 'Could not validate API key'
        )
