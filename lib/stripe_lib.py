import os
import stripe
from dotenv import load_dotenv

class Stripe_Lib:
    def __init__(self):
        load_dotenv(override = True)
        self.stripe = stripe
        self.stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    def get_all_prices(self):
        price_list = self.stripe.Price.list(active=True, limit=100, expand=['data.product', 'data.currency_options'])
        print(price_list)
        # prices = {}
        # currencies = set()

        # for price in price_list.data:
        #     if not price.recurring:
        #         continue

        #     product = price.product
        #     if not getattr(product.metadata, 'dev_plan_code', None):
        #         continue

        #     recurrence = 'monthly' if price.recurring.interval == 'month' else 'yearly'
        #     type_code = product.metadata.dev_plan_code

        #     if type_code not in prices:
        #         prices[type_code] = {'monthly': {'amount': {}, 'priceId': None}, 'yearly': {'amount': {}, 'priceId': None}}

        #     plan_price = prices[type_code][recurrence]
        #     plan_price['priceId'] = price.id

        #     for currency, option in price.currency_options.items():
        #         plan_price['amount'][currency] = option.unit_amount / 100
        #         currencies.add(currency)

        # return {
        #     "currencies": list(currencies),
        #     "prices": prices
        # }

    def get_all_products(self):
        return stripe.Product.list()
    
    def get_all_plans(self):
        return stripe.Plan.list()
    

if __name__ == "__main__":
    stripe_lib = Stripe_Lib()
    print(stripe_lib.get_all_products())
    print(stripe_lib.get_all_prices())
