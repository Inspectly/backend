import stripe
from fastapi import APIRouter, HTTPException, Header, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from app.crud.issue_offers import get_one as get_issue_offer_by_id, get_all_by_issue_id as get_all_offers_for_issue_id, update as update_offer 
from app.crud.issues import get_one as get_issue_by_id, update as update_issue
import os

from app.schema.properties import Issue_Offers, Issues

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

class CheckoutSessionRequest(BaseModel):
    offerID: int

@router.post("/payments/create-checkout-session")
async def create_checkout_session(data: CheckoutSessionRequest):
    # Step 1: Fetch offer from DB
    offer = get_issue_offer_by_id(data.offerID) ## look at what offerid would be in db
    
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    if offer["status"] == "accepted":
        raise HTTPException(status_code=400, detail="Offer already accepted")
    
    if offer["status"] == "rejected":
        raise HTTPException(status_code=400, detail="Offer already rejected")

    # Step 2: Calculate Stripe-compatible amount
    amount_cents = int(round(float(offer["price"]) * 100))

    # Step 3: Create Stripe Checkout session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Payment for offer #{offer['id']}",
                    },
                    "unit_amount": amount_cents,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{os.getenv('FRONTEND_BASE_URL')}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_BASE_URL')}/payment-cancel",
            metadata={
                "offer_id": str(offer["id"])
            }
        )
        return {"sessionUrl": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payments/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
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

    # Step 2: Handle only completed checkout sessions
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        offer_id = session["metadata"].get("offer_id")

        if not offer_id:
            print("⚠️ Webhook missing offer_id in metadata")
            return JSONResponse(status_code=400, content={"status": "missing offer_id"})

        try:
            # Step 3: Fetch the offer and issue
            offer = get_issue_offer_by_id(int(offer_id))
            if not offer:
                raise Exception("Offer not found")
            

            issue_id = offer["issue_id"]
            vendor_id = offer["vendor_id"]

            issue = get_issue_by_id(issue_id)
            if not issue:
                raise Exception("Issue not found")
            
            # accepting the offer
            offer["status"] = "accepted"
            offer_input = Issue_Offers(**{k: offer[k] for k in Issue_Offers.model_fields if k in offer}) #converting dict to model 
            update_offer(offer["id"], offer_input)

            # rejecting all other offers
            all_offers = get_all_offers_for_issue_id(issue_id)
            for o in all_offers:
                if o["id"] != offer["id"] and o["status"] not in ["rejected", "accepted"]:
                    o["status"] = "rejected"
                    o_input = Issue_Offers(**{k: o[k] for k in Issue_Offers.model_fields if k in o}) #converting dict to model
                    update_offer(o["id"], o_input)

            # update issue to assign vendor from the accepted offer
            issue["vendor_id"] = vendor_id
            issue_input = Issues(**{k: issue[k] for k in Issues.model_fields if k in issue}) #converting dict to model
            update_issue(issue_id, issue_input)

        except Exception as e:
            return JSONResponse(status_code=500, content={"status": "db error"})
        
        print(f"Offer {offer_id} accepted, vendor {vendor_id} set on issue {issue_id}")
        return JSONResponse(status_code=200, content={"status": "success"})

