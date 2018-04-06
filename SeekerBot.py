import time
from exceptions import PagiationException, ExecutedTrade
from constants import *
from Exchange import *
from Seeker import *

import keyboard
     

if __name__ == "__main__":
    s = Seeker("BTC_USD", 0.001, 0.01)
    while True:
        try:
            time.sleep(1)
            s.check_for_arb()
        except ExecutedTrade:
            break
        except PagiationException:
            s.logger.warn("Pagiation Exception")
        except KeyboardInterrupt:
            s.logger.warn("Keyboard interruption")
            break
