import logfire

from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Header, Request
from stripe.util import os

from app.core.stripe.stripe_webhook import Stripe_Webhook
from app.core.stripe.stripe_session import Stripe_Session
from app.core.stripe.types import Checkout_Session_Request

router = APIRouter()

@router.post('/checkout/create-session')
async def create_checkout_session(data: Checkout_Session_Request):
    try:
        stripe_session = Stripe_Session()
        session_url, session = await stripe_session.checkout_session(data)
        return {
            'session_url': session_url,
            'session': session
        }
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code = 404, detail = str(e))
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except RuntimeError as e:
        raise HTTPException(status_code = 500, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f'Unexpected error: {e}')

@router.post('/checkout/webhook')
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    logfire.configure(token = os.environ.get('LOGFIRE_API_KEY'), service_name = 'stripe_webhook', local = True)
    logfire.log(f'request: {request}')
    try:
        stripe_webhook = Stripe_Webhook()
        payload = await request.body()
        result = await stripe_webhook.webhook(payload, stripe_signature)
        return JSONResponse(status_code = 200, content = {'status': result['status']})
    except HTTPException:
        raise
    except ValueError as e:
        return JSONResponse(status_code = 400, content = {'status': 'error', 'detail': str(e)})
    except RuntimeError as e:
        return JSONResponse(status_code = 500, content = {'status': 'error', 'detail': str(e)})
    except Exception as e:
        return JSONResponse(status_code = 500, content = {'status': 'error', 'detail': 'Internal server error'})
