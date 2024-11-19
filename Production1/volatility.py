#===== Standard Library
#===== 3rd party
import numpy as np
#===== Reader
from ftx_helper import Ftx_Helper
#=====
class Volatility:
    def __init__(self, acc_type):
        self.helper = Ftx_Helper(acc_type=acc_type)
        
    def price_volatility_sum(self, positions_dict):
        vol_sum = 0
        for ticker in positions_dict.keys():
            current_price = self.helper.get_current_price(ticker)
            price_std = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=24)['close'].std()
            vol_sum += price_std * positions_dict[ticker]
        return vol_sum
        
    def volatility_scalar(self, ticker, daily_percent_volatility_target):
        #=====
        current_price = self.helper.get_current_price(ticker)
        price_std = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=24)['close'].std()
        instrument_value_volatility = price_std
        #=====
        daily_cash_volatility_target = self.helper.get_wallet_balance() * daily_percent_volatility_target  # could change wallet
        volatility_scalar = daily_cash_volatility_target / instrument_value_volatility
        return volatility_scalar