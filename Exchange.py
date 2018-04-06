from constants import *
from exceptions import PagiationException

class Exchange(object):
    def __init__(self, name, pair):
        self.name = name
        self.product_code = self.get_product_code(pair)
        self.maker_fee = fee_map[self.name]['maker']
        self.taker_fee = fee_map[self.name]['taker']

    def get_product_code(self, pair):
        return symbol_map[self.name][pair]

    def get_WA_price(self, side, trade_size, maker_taker):
        '''side = bid or ask'''
        self.set_order_book()
        i, r_qty, r_cost = 0, 0, 0
        try:
            while r_qty < trade_size:
                order = self.order_book[side][i]
                p = float(order[0])
                q = min(trade_size - r_qty, float(order[1]))
                r_qty +=q       # add to running quantity
                r_cost += p*q   # add to running cost
                i +=1
        except IndexError:
            raise PagiationException
        fee = self.maker_fee if maker_taker == 'maker' else self.taker_fee
        disc = (1+fee) if side == 'ask' else (1-fee)
        return {'WA_price': r_cost/r_qty,
                'limit_price': p,
                'Eff_price': disc * r_cost/r_qty}
