import os
import stripe

from app.core.stripe.types import Checkout_Session_Request
from app.core.stripe.serializer import validate_issue_offer, validate_user

class Stripe_Session:
    def __init__(self):
        self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        self.frontend_base_url = os.getenv('FRONTEND_BASE_URL')
        self.stripe = stripe
        self.stripe.api_key = self.stripe_secret_key

    def checkout_session(self, data: Checkout_Session_Request):
        valid_client = validate_user(data.client_id)
        valid_vendor = validate_user(data.vendor_id)
        valid_offer = validate_issue_offer(data.offer_id)
        try:
            session = self.stripe.checkout.Session.create(
                line_items = [
                    {
                        'price_data': {
                            'currency': 'cad',
                            'unit_amount': int(round(float(valid_offer['price']) * 100)),
                            'product_data': {
                                'name': f'Payment for offer #{valid_offer['id']}'
                            }
                        },
                        'quantity': 1
                    }
                ],
                customer = valid_client['stripe_user_id'], # person making the payment
                mode = 'payment',
                payment_method_types = ['card'],
                success_url = f'{self.frontend_base_url}/listings/{valid_offer['listing_id']}/reports/{valid_offer['report_id']}/issues/{valid_offer['issue_id']}?tab=offers&payment=success&session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url = f'{self.frontend_base_url}/listings/{valid_offer['listing_id']}/reports/{valid_offer['report_id']}/issues/{valid_offer['issue_id']}?tab=offers&payment=failed',
                metadata = {
                    'offer_id': str(valid_offer['id']),
                    'client_id': str(valid_client['user_id']),
                    'vendor_id': str(valid_vendor['user_id'])
                }
            )
            return session.url, session
        except Exception as e:
            raise RuntimeError(f'Internal server error: {e}')

    def webhook(self):
        pass