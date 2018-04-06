from pybitflyer import API as BitFlyer_API
from constants import *
from Exchange import *
from Seeker import *
import config

class BitFlyer(Exchange, BitFlyer_API):
    def __init__(self, pair):
        Exchange.__init__(self, 'BitFlyer', pair)
        BitFlyer_API.__init__(self, api_key=config.key_pairs[self.name][KEY],
                              api_secret=config.key_pairs[self.name][SECRET])
        self.set_order_book()

    def set_order_book(self):
        resp = self.board(product_code=self.product_code)
        ob = {'bid': [[a['price'], a['size']] for a in resp['bids']],
              'ask': [[a['price'], a['size']] for a in resp['asks']]}
        self.order_book = ob

    def market_buy(self, qty):
        resp = self.sendchildorder(product_code=self.product_code, child_order_type="MARKET", side="BUY", size=qty)
        return resp['child_order_acceptance_id']

    def market_sell(self, qty):
        resp = self.sendchildorder(product_code=self.product_code, child_order_type="MARKET", side="SELL", size=qty)
        return resp['child_order_acceptance_id']

    def get_order(self, id):
        return self.getexecutions(product_code=self.product_code, child_order_acceptance_id=id)
    
    def limit_buy(self, qty, price, time_in_force):
        return self.sendchildorder(product_code=self.product_code, size=qty, price=price, side="BUY",
                                   child_order_type='LIMIT', time_in_force=time_in_force)

    def limit_sell(self, qty, price, time_in_force):
        return self.sendchildorder(product_code=self.product_code, size=qty, price=price, side="SELL",
                                   child_order_type='LIMIT', time_in_force=time_in_force)