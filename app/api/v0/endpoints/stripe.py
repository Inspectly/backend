from datetime import datetime, timezone
import stripe
from fastapi import APIRouter, HTTPException, Header, Request
from starlette.responses import JSONResponse

from app.crud.issue_offers import get_one as get_issue_offer_by_id, get_all_by_issue_id as get_all_offers_for_issue_id, update as update_offer 
from app.crud.issues import get_one as get_issue_by_id, update as update_issue
import os

from app.schema.properties import Issue_Offers, Issues
from app.schema.types import Status
from app.core.stripe.stripe_session import Stripe_Session
from app.core.stripe.types import Checkout_Session_Request

router = APIRouter()

@router.post('/create-checkout-session')
async def create_checkout_session(data: Checkout_Session_Request):
    try:
        stripe_session = Stripe_Session()
        session_url, session = stripe_session.checkout_session(data)
        return {
            'session_url': session_url,
            'session': session
        }
    except LookupError as e:
        raise HTTPException(status_code = 404, detail = str(e))
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))
    except RuntimeError as e:
        raise HTTPException(status_code = 500, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f'Unexpected error: {e}')

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    print("stripe webhook initiated")
    payload = await request.body()
    stripe_webhook_secret = os.getenv('STRIPE_WEBHOOK')
    # Step 1: Verify Stripe signature
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]
    session = event["data"]["object"]

    if event_type in ["checkout.session.completed", "checkout.session.async_payment_succeeded"]:
        offer_id = session["metadata"].get("offer_id")
        print(f"Payment success event received: {event_type}, offer_id={offer_id}")

        if not offer_id:
            print("Webhook missing offer_id in metadata")
            return JSONResponse(status_code=400, content={"status": "missing offer_id"})
        
        try:
            offer = get_issue_offer_by_id(int(offer_id))
            if not offer:
                raise Exception("Offer not found")

            issue_id = offer["issue_id"]
            vendor_id = offer["vendor_id"]

            issue = get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")


            offer["status"] = "accepted"
            offer["user_last_viewed"] = datetime.now(timezone.utc).isoformat()
            offer_input = Issue_Offers(**{k: offer[k] for k in Issue_Offers.model_fields if k in offer})
            update_offer(offer["id"], offer_input)

            all_offers = get_all_offers_for_issue_id(issue_id)
            for o in all_offers:
                if o["id"] != offer["id"] and o["status"] not in ["rejected", "accepted"]:
                    o["status"] = "rejected"
                    o["user_last_viewed"] = datetime.now(timezone.utc).isoformat()
                    o_input = Issue_Offers(**{k: o[k] for k in Issue_Offers.model_fields if k in o})
                    update_offer(o["id"], o_input)

            issue["vendor_id"] = vendor_id
            issue["status"] = Status.IN_PROGRESS
            issue_input = Issues(**{k: issue[k] for k in Issues.model_fields if k in issue})
            update_issue(issue_id, issue_input)

            print(f"Offer {offer_id} accepted, vendor {vendor_id} assigned to issue {issue_id}")
        except Exception as e:
            print(f"Webhook DB error: {e}")
            return JSONResponse(status_code=500, content={"status": "updating db error"})

    elif event_type in ["checkout.session.async_payment_failed", "checkout.session.expired"]:
        print(f"Payment did not complete: {event_type}, session_id={session['id']}")

        # TODO add log to DB, currently logging through print statements

    else:
        print(f"Unhandled Stripe event: {event_type}")

    return JSONResponse(status_code=200, content={"status": "success"})

