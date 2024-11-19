#===== Standard Library
#===== 3rd party
import pandas as pd
import numpy as np
#===== Reader
from ftx_helper import Ftx_Helper
#=====
class Tsmom:
    def __init__(self, acc_type):
        self.helper = Ftx_Helper(acc_type=acc_type)
    
    def forecast(self, period_days, ticker):
        period_hours = 24 * period_days
        kline_df = self.helper.get_kline(ticker=ticker, interval='1h', since=None, limit=period_hours)
        baseline_price = kline_df.iloc[0]['close']
        today_price = kline_df.iloc[-1]['close']
        return np.sign(today_price - baseline_price)
    
    def volatility_scalar(self, period_days, ticker, price_vol_target):
        volatility_measure = 25
        price_std = self.helper.get_kline(ticker=ticker, interval='1d', since=None, limit=volatility_measure)['close'].std()
        instrument_value_volatility = price_std
        #=====
        volatility_scalar = price_vol_target / instrument_value_volatility
        return volatility_scalar
        