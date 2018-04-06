import logging
import time
import keyboard
from exceptions import ExecutedTrade
from Bitflyer import BitFlyer
from GDAX import GDAX
import config

class Seeker(object):
    def __init__(self, pair, trade_size, profit_per_trade):
        self.pair = pair
        self.trade_size = trade_size
        self.profit_per_trade = profit_per_trade
        self.ex_seller = BitFlyer(self.pair)
        self.ex_buyer = GDAX(self.pair)
        self.logger = self.create_logger()
        self.add_hotkeys()

    def create_logger(self):
        logger = logging.Logger(__name__, level=logging.DEBUG)
        '''
        # Log warning to log.log file
        fileHandler = logging.FileHandler('log.log')
        fileHandler.setLevel(logging.WARN)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        '''
        # Log debug messages to console
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s:%(message)s')
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        return logger

    def add_hotkeys(self):
        keyboard.add_hotkey('-+s', self.switch_buyer_seller)

    def check_for_arb(self):
        # Buy BTC with GDAX (FOK - maker)
        buy_price = self.ex_buyer.get_WA_price("ask", self.trade_size, 'taker')
        self.logger.info("{} {}:\t{}".format("Buyer ", self.ex_buyer.name, buy_price))
        # sell BTC with BitFlyer (market)
        sell_price = self.ex_seller.get_WA_price("bid", self.trade_size, 'taker')
        self.logger.info("{} {}:\t{}".format("Seller", self.ex_seller.name, sell_price))

        Eff_profit = sell_price['Eff_price'] / buy_price['Eff_price'] - 1
        self.logger.info(Eff_profit)
        if Eff_profit > self.profit_per_trade:
            self.execute_trade(limit_buy=buy_price['limit_price'])
    
    def execute_trade(self, limit_buy):
        if config.live == False:
            self.logger.info("Would have bought at {}".format(limit_buy))
            self.switch_buyer_seller()
            return
        buy_info = self.ex_buyer.limit_buy(self.trade_size, limit_buy, 'FOK')
        while buy_info['status'] =='pending':
            time.sleep(0.17)
            buy_info = self.ex_buyer.get_order(buy_info['id'])
        if buy_info['status'] == 'done':
            sell_info = self.ex_seller.market_sell(self.trade_size)
            time.sleep(3)
            sell_info = self.ex_seller.get_order(sell_info)
            raise ExecutedTrade(buy_info, sell_info)
        elif buy_info['status'] != 'rejected':
            self.ex_buyer.cancel_order(buy_info['id'])
        else:
            self.logger.info('Order was rejected {}'.format(str(buy_info)))

    def switch_buyer_seller(self):
        self.ex_buyer, self.ex_seller = self.ex_seller, self.ex_buyer
        self.logger.info("Switching buyer and seller.\nBuyer = {}, Seller = {}".format(
            self.ex_buyer.name, self.ex_seller.name))
        time.sleep(10)