import os
import logfire
import stripe
from datetime import datetime, timezone

from app.schema.types import Status, Bid_Status
from app.schema.properties import Issue_Offers, Issues
from app.core.stripe.types import Stripe_Checkout_Session
from app.core.stripe.serializer import validate_webhook_metadata
from app.crud.issue_offers import (
    update as update_offer,
    get_all_by_issue_id as get_all_offers_for_issue_id,
)
from app.crud.issues import (
    update as update_issue,
)

class Stripe_Webhook:
    def __init__(self):
        self.stripe_webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        logfire.configure(token = os.getenv('LOGFIRE_API_KEY'), service_name = 'stripe_webhook', scrubbing=False)
    
    async def _validate_webhook(self, payload, stripe_signature: str):
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, self.stripe_webhook_secret
            )
            logfire.info(f'event: {event}')
            return event
        except ValueError:
            raise ValueError('Invalid payload')
        except stripe.error.SignatureVerificationError:
            raise ValueError('Invalid signature')
        except Exception as e:
            raise RuntimeError(f'Internal server error: {e}')
    
    async def webhook(self, payload, stripe_signature: str):
        logfire.info(f'payload: {payload}')
        logfire.info(f'stripe_signature: {stripe_signature}')
        event = await self._validate_webhook(payload, stripe_signature)
        logfire.info(f'event: {event}')
        event_type = event['type']
        session = event['data']['object']
        logfire.info(f'event_type: {event_type}')
        logfire.info(f'session: {session}')

        if (event_type == Stripe_Checkout_Session.COMPLETED or event_type == Stripe_Checkout_Session.PAYMENT_SUCCEEDED):
            try:
                offer_id, client_id, vendor_id, offer, issue, issue_id = validate_webhook_metadata(session)
                logfire.info(f'offer_id: {offer_id}')
                logfire.info(f'client_id: {client_id}')
                logfire.info(f'vendor_id: {vendor_id}')
                logfire.info(f'offer: {offer}')
                logfire.info(f'issue: {issue}')
                logfire.info(f'issue_id: {issue_id}')
                all_offers = get_all_offers_for_issue_id(issue_id)
                for current_offer in all_offers:
                    if (current_offer['id'] == int(offer_id)):
                        current_offer['status'] = Bid_Status.ACCEPTED
                        current_offer['user_last_viewed'] = datetime.now(timezone.utc).isoformat()
                        updated_offer = Issue_Offers(**{k: current_offer[k] for k in Issue_Offers.model_fields if k in current_offer})
                        logfire.info(f'updated_offer: {updated_offer}')
                        update_offer(current_offer['id'], updated_offer)
                    elif (current_offer['id'] != int(offer_id) and current_offer['status'] not in ['rejected', 'accepted']):
                        current_offer['status'] = Bid_Status.REJECTED
                        current_offer['user_last_viewed'] = datetime.now(timezone.utc).isoformat()
                        updated_offer = Issue_Offers(**{k: current_offer[k] for k in Issue_Offers.model_fields if k in current_offer})
                        logfire.info(f'updated_offer: {updated_offer}')
                        update_offer(current_offer['id'], updated_offer)
                        

                issue['vendor_id'] = vendor_id
                issue['status'] = Status.IN_PROGRESS
                issue_input = Issues(**{k: issue[k] for k in Issues.model_fields if k in issue})
                logfire.info(f'issue_input: {issue_input}')
                update_issue(issue_id, issue_input)

                return {'status': f'stripe payment from {client_id} for offer {offer_id} successful'}

            except Exception as e:
                raise RuntimeError(f'Database error for event {event_type}: {e}')

        elif (event_type == Stripe_Checkout_Session.PAYMENT_FAILED or event_type == Stripe_Checkout_Session.EXPIRED):
            return {'status': f'stripe payment from {client_id} for offer {offer_id} unsuccessful. {event_type}'}

        else:
            return {'status': f'unhandled event type: {event_type}'}
