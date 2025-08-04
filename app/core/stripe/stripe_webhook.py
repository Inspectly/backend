import os
import stripe
from datetime import datetime, timezone

from app.schema.types import Status
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
    
    async def _validate_webhook(self, payload, stripe_signature: str):
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, self.stripe_webhook_secret
            )
            return event
        except ValueError:
            raise ValueError('Invalid payload')
        except stripe.error.SignatureVerificationError:
            raise ValueError('Invalid signature')
        except Exception as e:
            raise RuntimeError(f'Internal server error: {e}')
    
    async def webhook(self, payload, stripe_signature: str):
        event = self._validate_webhook(payload, stripe_signature)
        event_type = event['type']
        session = event['data']['object']

        if (event_type == Stripe_Checkout_Session.COMPLETED or event_type == Stripe_Checkout_Session.PAYMENT_SUCCEEDED):
            try:
                offer_id, client_id, vendor_id, offer, issue, issue_id = validate_webhook_metadata(session)

                all_offers = get_all_offers_for_issue_id(issue_id)
                for current_offer in all_offers:
                    if (current_offer['id'] == int(offer_id)):
                        current_offer['status'] = 'accepted'
                        current_offer['user_last_viewed'] = datetime.now(timezone.utc).isoformat()
                        updated_offer = Issue_Offers(**{k: current_offer[k] for k in Issue_Offers.model_fields if k in current_offer})
                        update_offer(current_offer['id'], updated_offer)
                    elif (current_offer['id'] != int(offer_id) and current_offer['status'] not in ['rejected', 'accepted']):
                        current_offer['status'] = 'rejected'
                        current_offer['user_last_viewed'] = datetime.now(timezone.utc).isoformat()
                        updated_offer = Issue_Offers(**{k: current_offer[k] for k in Issue_Offers.model_fields if k in current_offer})
                        update_offer(current_offer['id'], updated_offer)

                issue['vendor_id'] = vendor_id
                issue['status'] = Status.IN_PROGRESS.value
                issue_input = Issues(**{k: issue[k] for k in Issues.model_fields if k in issue})
                update_issue(issue_id, issue_input)

                return {'status': f'stripe payment from {client_id} for offer {offer_id} successful'}

            except Exception as e:
                raise RuntimeError(f'Database error for event {event_type}: {e}')

        elif (event_type == Stripe_Checkout_Session.PAYMENT_FAILED or event_type == Stripe_Checkout_Session.EXPIRED):
            return {'status': f'stripe payment from {client_id} for offer {offer_id} unsuccessful. {event_type}'}

        else:
            return {'status': f'unhandled event type: {event_type}'}
