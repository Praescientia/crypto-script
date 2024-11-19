#===== Standard Library
#===== 3rd party
import numpy as np
#===== Reader
from ftx_futures_exchange_helper import Ftx_Futures_Exchange_Helper
#=====
class Trader:
    def __init__(self, acc_type):
        self.helper = Ftx_Futures_Exchange_Helper(acc_type=acc_type)
    
    def liquidate(self, ticker):
        position_qty = self.helper.get_position(ticker)
        if np.sign(position_qty) < 0:
            resp = self.helper.create_marketprice_order(ticker=ticker, qty=abs(position_qty), order_type='buy', reduce_only=True)
        elif np.sign(position_qty) > 0:
            resp = self.helper.create_marketprice_order(ticker=ticker, qty=abs(position_qty), order_type='sell', reduce_only=True)
        else:
            print("QTY already 0")
    