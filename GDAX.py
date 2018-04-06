from gdax import AuthenticatedClient as GDAX_API
from constants import *
from Exchange import *
from Seeker import *
import config

class GDAX(Exchange, GDAX_API):
    def __init__(self, pair):
        Exchange.__init__(self, 'GDAX', pair)
        GDAX_API.__init__(self, key=config.key_pairs[self.name][KEY],
                           b64secret=config.key_pairs[self.name][SECRET],
                           passphrase=config.key_pairs[self.name][PASSPHRASE])
        self.set_order_book()


    def set_order_book(self):
        resp = self.get_product_order_book(self.product_code, level=2)
        ob = {'bid': [a[:2] for a in resp['bids']],
              'ask': [a[:2] for a in resp['asks']]}
        self.order_book = ob
    
    def market_buy(self, qty):
        return self.buy(product_id=self.product_code, size=qty, type='market')

    def market_sell(self, qty):
        return self.sell(product_id=self.product_code, size=qty, type='market')

    def limit_buy(self, qty, price, time_in_force):
        return self.buy(product_id=self.product_code, size=qty, price=price,
                        type='limit', time_in_force=time_in_force)

    def limit_sell(self, qty, price, time_in_force):
        return self.sell(product_id=self.product_code, size=qty, price=price,
                         type='limit', time_in_force=time_in_force)

