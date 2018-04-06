class PagiationException(IndexError):
    IndexError()

class ExecutedTrade(Exception):
    def __init__(self, buy_info, sell_info):
        print(buy_info)
        print(sell_info)
        Exception()
